import pandas as pd
import numpy as np
import random
import requests
import json
import time
import re
from typing import Dict, List
from geopy.distance import geodesic
# from config import API_KEY_Groq
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import concurrent.futures
import math
from sse_starlette.sse import EventSourceResponse
import asyncio
from fastapi.routing import APIRouter
import os

API_KEY_Groq = 'YOUR_API_KEY'

path = os.path.dirname(os.path.abspath(__file__))
df_path = os.path.join(path, "..", "data", "dc_businesses_cleaned.csv")

if not API_KEY_Groq or len(API_KEY_Groq.strip()) < 20:
    raise ValueError("""
    Invalid or missing Groq API key. 
    Make sure your config.py file contains a valid API_KEY_Groq value.
    """)

# Updated Merchant category mapping
CATEGORY_MAPPING = {
    # Food & Grocery
    "Grocery Store": "groceries",
    "Delicatessen": "deli_prepared_foods",
    "Bakery": "bakery",
    "Food Products": "packaged_foods",
    "Food Vending Machine": "vending_snacks",
    "Ice Cream Manufacture": "ice_cream",
    "Marine Food Retail": "seafood_market",
    "Mobile Delicatessen": "food_truck",

    # Dining
    "Restaurant": "restaurant_dining",
    "Caterers": "catering_services",

    # Transportation
    "Gasoline Dealer": "gas_station",
    "Auto Rental": "car_rental",
    "Auto Wash": "car_wash",
    "Tow Truck": "towing_services",
    "Tow Truck Business": "towing_company",
    "Tow Truck Storage Lot": "vehicle_storage",
    "Driving School": "driving_lessons",

    # Entertainment
    "Motion Picture Theatre": "movie_theater",
    "Public Hall": "event_venue",
    "Theater (Live)": "live_theater",
    "Bowling Alley": "bowling",
    "Billiard Parlor": "pool_hall",
    "Skating Rink": "skating_rink",
    "Athletic Exhibition": "sports_events",
    "Special Events": "special_events",

    # Lodging
    "Hotel": "hotel_lodging",
    "Inn And Motel": "motel_lodging",
    "Bed and Breakfast": "bnb_lodging",
    "Vacation Rental": "vacation_rental",
    "Boarding House": "boarding_house",

    # Personal Care
    "Beauty Shop": "beauty_services",
    "Barber Shop": "barber_services",
    "Beauty Booth": "beauty_booth",
    "Beauty Shop Braiding": "hair_braiding",
    "Beauty Shop Electrology": "electrolysis",
    "Beauty Shop Esthetics": "skin_care",
    "Beauty Shop Nails": "nail_salon",
    "Health Spa": "spa_services",
    "Massage Establishment": "massage_parlor",
}

# Approximate coordinates for DC ZIP codes
DC_ZIP_COORDS = {
    '20001': (38.9109, -77.0163),
    '20002': (38.9123, -77.0127),
    '20003': (38.8857, -76.9894),
    '20004': (38.8951, -77.0366),
    '20005': (38.9026, -77.0311),
    '20006': (38.8979, -77.0369),
    '20007': (38.9183, -77.0709),
    '20008': (38.9368, -77.0595),
    '20009': (38.9193, -77.0374),
    '20010': (38.9327, -77.0294),
    '20011': (38.9566, -77.0232),
    '20012': (38.9770, -77.0296),
    '20015': (38.9664, -77.0846),
    '20016': (38.9346, -77.0896),
    '20017': (38.9348, -76.9886),
    '20018': (38.9238, -76.9894),
    '20019': (38.8898, -76.9488),
    '20020': (38.8641, -76.9857),
    '20024': (38.8743, -77.0167),
    '20032': (38.8458, -77.0013),
    '20036': (38.9055, -77.0417),
    '20037': (38.8996, -77.0527),
    '20052': (38.8990, -77.0479),
    '20057': (38.9087, -77.0731),
    '20064': (38.9335, -76.9978),
}


class TransactionGenerator:
    def __init__(self, api_key: str, merchants_df: pd.DataFrame):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.merchants = merchants_df
        self._preprocess_merchants()
        
        # Add merchant caching
        self._merchant_cache = {}
        self._category_merchant_cache = {}
        
        self.spending_categories = {
            # Food & Grocery
            "groceries": 0.14,
            "deli_prepared_foods": 0.02,
            "bakery": 0.02,
            "packaged_foods": 0.02,
            "vending_snacks": 0.01,
            "ice_cream": 0.01,
            "seafood_market": 0.02,
            "food_truck": 0.02,

            # Dining
            "restaurant_dining": 0.10,
            "catering_services": 0.02,

            # Transportation
            "gas_station": 0.05,
            "car_rental": 0.01,
            "car_wash": 0.01,
            "towing_services": 0.00,
            "towing_company": 0.00,
            "vehicle_storage": 0.00,
            "driving_lessons": 0.01,

            # Entertainment
            "movie_theater": 0.03,
            "event_venue": 0.02,
            "live_theater": 0.01,
            "bowling": 0.01,
            "pool_hall": 0.01,
            "skating_rink": 0.01,
            "sports_events": 0.02,
            "special_events": 0.02,

            # Lodging
            "hotel_lodging": 0.04,
            "motel_lodging": 0.02,
            "bnb_lodging": 0.01,
            "vacation_rental": 0.02,
            "boarding_house": 0.01,

            # Personal Care
            "beauty_services": 0.03,
            "barber_services": 0.02,
            "beauty_booth": 0.00,
            "hair_braiding": 0.00,
            "electrolysis": 0.00,
            "skin_care": 0.01,
            "nail_salon": 0.01,
            "spa_services": 0.02,
            "massage_parlor": 0.01
        }

        # Update transaction scaling parameters for monthly data
        self.MIN_TRANSACTIONS_PER_DAY = 2
        self.MAX_TRANSACTIONS_PER_DAY = 8
        self.BASE_INCOME = 50000

    def _preprocess_merchants(self):
        """Clean and prepare merchant data"""
        try:
            print("\n=== Preprocessing Merchants ===")
            print(f"Initial merchant count: {len(self.merchants)}")
            print("Initial columns:", self.merchants.columns.tolist())

            # Rename columns
            column_map = {
                'ENTITY_NAME': 'Name',
                'LICENSECATEGORY': 'Category',
                'ZIP': 'Zipcode',
                'LATITUDE': 'Latitude',
                'LONGITUDE': 'Longitude'
            }
            self.merchants = self.merchants.rename(columns=column_map)
            print("\nColumns after renaming:", self.merchants.columns.tolist())

            # Set default coordinates
            if 'Latitude' not in self.merchants.columns:
                self.merchants['Latitude'] = 38.9072
                print("Added default Latitude")
            if 'Longitude' not in self.merchants.columns:
                self.merchants['Longitude'] = -77.0369
                print("Added default Longitude")

            # Map categories
            print("\nMapping categories...")
            print("Original categories sample:", self.merchants['Category'].unique()[:5])
            
            self.merchants['mapped_category'] = (
                self.merchants['Category']
                .map(CATEGORY_MAPPING)
                .fillna('other')
            )
            
            print("Mapped categories sample:", self.merchants['mapped_category'].unique()[:5])
            print(f"Total unique mapped categories: {self.merchants['mapped_category'].nunique()}")

            # Clean zipcode
            print("\nCleaning zipcodes...")
            self.merchants['Zipcode'] = (
                self.merchants['Zipcode']
                .astype(str)
                .str.extract(r'(\d{5})')[0]
                .fillna('20001')
            )
            
            print("Sample zipcodes:", self.merchants['Zipcode'].unique()[:5])
            print(f"\nFinal merchant count: {len(self.merchants)}")
            
            # Show sample of processed data
            print("\nSample of processed merchants:")
            print(self.merchants[['Name', 'Category', 'mapped_category', 'Zipcode']].head())

        except Exception as e:
            print(f"Error in preprocessing merchants: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise

    def _get_merchant(self, category: str, zipcode: str) -> Dict:
        """Get merchant with caching"""
        cache_key = f"{category}:{zipcode}"
        
        # Check category cache first
        if category not in self._category_merchant_cache:
            self._category_merchant_cache[category] = self.merchants[
                self.merchants['mapped_category'] == category
            ].to_dict('records')
        
        # Check specific merchant cache
        if cache_key not in self._merchant_cache:
            merchants = [m for m in self._category_merchant_cache[category] 
                       if str(m['Zipcode']).startswith(str(zipcode)[:3])]
            if not merchants:  # Fallback to any merchant in category
                merchants = self._category_merchant_cache[category]
            self._merchant_cache[cache_key] = merchants

        merchants = self._merchant_cache[cache_key]
        return random.choice(merchants) if merchants else self._create_fallback_merchant(category, zipcode)

    def _calculate_transaction_count(self, income: float, days: int = 30) -> int:
        """Calculate monthly transactions based on income with reasonable limits"""
        # Base transaction counts per month
        MIN_MONTHLY_TRANSACTIONS = 20  # Minimum 20 transactions per month
        MAX_MONTHLY_TRANSACTIONS = 60  # Maximum 60 transactions per month
        
        # Calculate based on income brackets
        if income < 30000:
            base_count = MIN_MONTHLY_TRANSACTIONS
        elif income < 50000:
            base_count = 30
        elif income < 75000:
            base_count = 40
        elif income < 100000:
            base_count = 50
        else:
            base_count = MAX_MONTHLY_TRANSACTIONS
        
        # Add small random variation (±10%)
        variation = random.uniform(-0.1, 0.1)
        final_count = int(base_count * (1 + variation))
        
        # Ensure within bounds
        return max(MIN_MONTHLY_TRANSACTIONS, min(final_count, MAX_MONTHLY_TRANSACTIONS))

    def _get_nearby_merchants(self, base_zip: str, max_distance: int = 2) -> List[Dict]:
        """Find merchants within 'max_distance' miles using geodesic distance."""
        clean_zip = str(int(float(base_zip))) if base_zip.replace('.', '').isdigit() else '20001'
        clean_zip = clean_zip[:5]
        base_coord = DC_ZIP_COORDS.get(clean_zip, DC_ZIP_COORDS['20001'])

        self.merchants['distance'] = self.merchants.apply(
            lambda row: geodesic(base_coord, (row['Latitude'], row['Longitude'])).miles,
            axis=1
        )
        return self.merchants[self.merchants['distance'] <= max_distance]

    def _assign_categories(self) -> list:
        """Random category assignment with income weighting"""
        base_prob = 0.7  # Base probability for essential categories
        return [
            cat for cat, prob in self.spending_categories.items()
            if random.random() < base_prob + (prob * 0.3)
        ]

    def _generate_spending_pattern(self, categories: list, income: float) -> dict:
        """Create spending distribution based on categories and income"""
        monthly_income = income / 12
        total_weight = sum(self.spending_categories[cat] for cat in categories)

        return {
            cat: (self.spending_categories[cat] / total_weight) * monthly_income
            for cat in categories
        }

    def _batch_generate_transactions(self, customer: dict, merchants: list, num_tx: int) -> List[dict]:
        try:
            # Remove print statements that aren't necessary
            current_date = time.strftime("%Y-%m-%d")
            merchant_examples = "\n".join([
                f'  - Name: "{m.get("Name", "")}", Category: "{m.get("Category", "")}"'
                for m in merchants[:3]
            ])
            
            prompt = f"""Generate exactly {num_tx} financial transactions as a JSON array.

Available Merchants:
{merchant_examples}

Requirements:
1. Use ONLY the provided merchants
2. Generate transactions for date: {current_date}
3. Amount range: $10.00 to $200.00
4. Use this EXACT JSON structure:
[
  {{
    "amount": 45.99,
    "timestamp": "{current_date}T10:30:00Z",
    "merchant_details": {{
      "name": "<exact merchant name from list>",
      "category": "<exact merchant category>",
      "zipcode": "{customer['zipcode']}"
    }},
    "payment_type": "credit_card"
  }}
]"""

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=self.headers,
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a precise JSON generator. Output only valid JSON arrays matching the exact specified format. No additional text or explanations."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.1,
                    "max_tokens": 1000,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return []

            try:
                response_json = response.json()
                content = response_json["choices"][0]["message"]["content"].strip()
                
                # Clean and parse JSON without debug output
                content = content.replace('\n', ' ').replace('\r', '')
                content = re.sub(r'```json|```', '', content)
                content = re.sub(r'[^\[\]\{\}",:.\d\w\s-]', '', content)
                
                match = re.search(r'\[.*\]', content)
                if not match:
                    return []
                
                transactions = json.loads(match.group(0))
                if not isinstance(transactions, list):
                    return []
                
                valid_transactions = []
                for tx in transactions:
                    if isinstance(tx, dict) and all(k in tx for k in ["amount", "timestamp", "merchant_details", "payment_type"]):
                        if isinstance(tx["merchant_details"], dict) and all(k in tx["merchant_details"] for k in ["name", "category", "zipcode"]):
                            try:
                                tx["amount"] = float(tx["amount"])
                                if 10 <= tx["amount"] <= 200:
                                    valid_transactions.append(tx)
                            except (ValueError, TypeError):
                                continue
                
                return valid_transactions

            except json.JSONDecodeError:
                return []
            
        except Exception:
            return []

    def generate_transactions(self, user_data: dict) -> list:
        """Main generation method with smaller batches"""
        try:
            print("\n=== Starting Transaction Generation ===")
            print(f"User data: {user_data}")

            # Create customer profile
            customer = {
                'customer_id': f"WEB-{random.randint(100000, 999999)}",
                **{k: str(user_data[k]) if k == 'zipcode' else user_data[k] for k in ['age', 'gender', 'household_size', 'income', 'zipcode']}
            }

            # Calculate transactions needed
            total_needed = self._calculate_transaction_count(float(user_data['income']), days=30)
            print(f"\nNeed to generate {total_needed} transactions")

            # Generate in very small batches
            all_transactions = []
            batch_size = 10 
            categories = self._assign_categories()

            while len(all_transactions) < total_needed:
                try:
                    current_batch_size = min(batch_size, total_needed - len(all_transactions))
                    merchants = [self._get_merchant(random.choice(categories), customer['zipcode']) 
                               for _ in range(current_batch_size)]
                    
                    batch_transactions = self._batch_generate_transactions(customer, merchants, current_batch_size)
                    if batch_transactions:
                        all_transactions.extend(batch_transactions)
                        print(f"Progress: {len(all_transactions)}/{total_needed} transactions")
                    
                    if not batch_transactions:
                        print("Batch generated no transactions, retrying...")
                    
                    time.sleep(1)  # Small delay between batches
                    
                except Exception as e:
                    print(f"Batch failed: {str(e)}")
                    continue

                if len(all_transactions) >= total_needed:
                    break

            print(f"\nFinished generating {len(all_transactions)} transactions")
            return all_transactions

        except Exception as e:
            print(f"Transaction generation failed: {str(e)}")
            return []


# First load the raw data
print("\n=== Loading Merchant Data ===")
print(f"CSV Path: {df_path}")
print(f"CSV exists: {os.path.exists(df_path)}")
if os.path.exists(df_path):
    print(f"CSV size: {os.path.getsize(df_path)} bytes")
    print("First few rows:")
    merchants_df_raw = pd.read_csv(df_path)
    print(merchants_df_raw.head())
else:
    raise FileNotFoundError(f"Merchant data file not found: {df_path}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("\n=== Raw Merchant Data Information ===")
    print(f"Total merchants loaded: {len(merchants_df_raw)}")
    print("\nSample merchants (raw data):")
    print(merchants_df_raw[['Name', 'Category', 'Zipcode']].head())
    print("\nUnique categories:", merchants_df_raw['Category'].nunique())
    
    yield
    
    # Shutdown
    print("\nShutting down application...")

# Update FastAPI initialization
app = FastAPI(lifespan=lifespan)

# Allow frontend to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-SSE"]
)

class UserInput(BaseModel):
    age: int
    gender: str
    household_size: int
    income: float
    zipcode: str


# Initialize generator with processed data
generator = TransactionGenerator(api_key=API_KEY_Groq, merchants_df=merchants_df_raw)


@app.route("/generate", methods=["GET", "POST"])
async def generate_transactions(request: Request):
    try:
        # Get parameters either from query params (GET) or request body (POST)
        if request.method == "GET":
            params = dict(request.query_params)
            user_data = {
                "age": int(params.get("age", 0)),
                "gender": params.get("gender", ""),
                "household_size": int(params.get("household_size", 0)),
                "income": float(params.get("income", 0)),
                "zipcode": params.get("zipcode", "")
            }
        else:  # POST
            user_data = await request.json()

        # Validate the data
        if not all([user_data.get("age"), user_data.get("gender"), 
                   user_data.get("household_size"), user_data.get("income"), 
                   user_data.get("zipcode")]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        async def event_generator():
            try:
                # Initial status
                yield {
                    "event": "status",
                    "data": json.dumps({
                        "message": "Starting transaction generation...",
                        "progress": 0,
                        "status": "initializing"
                    })
                }

                total_needed = generator._calculate_transaction_count(float(user_data['income']))
                yield {
                    "event": "status",
                    "data": json.dumps({
                        "message": f"Planning to generate {total_needed} transactions",
                        "total": total_needed,
                        "progress": 0,
                        "status": "planning"
                    })
                }

                all_transactions = []
                batch_size = 5
                categories = generator._assign_categories()

                batch_number = 0
                while len(all_transactions) < total_needed:
                    if await request.is_disconnected():
                        print("Client disconnected")
                        break

                    try:
                        current_batch_size = min(batch_size, total_needed - len(all_transactions))
                        merchants = [generator._get_merchant(random.choice(categories), user_data['zipcode']) 
                                   for _ in range(current_batch_size)]

                        yield {
                            "event": "status",
                            "data": json.dumps({
                                "message": f"Processing batch {batch_number + 1}",
                                "merchants": [m.get('Name') for m in merchants],
                                "progress": len(all_transactions),
                                "total": total_needed,
                                "status": "processing"
                            })
                        }

                        batch_transactions = generator._batch_generate_transactions(user_data, merchants, current_batch_size)
                        
                        if batch_transactions:
                            all_transactions.extend(batch_transactions)
                            yield {
                                "event": "batch_complete",
                                "data": json.dumps({
                                    "message": f"Completed batch {batch_number + 1}",
                                    "transactions": batch_transactions,
                                    "progress": len(all_transactions),
                                    "total": total_needed,
                                    "status": "batch_complete"
                                })
                            }
                        else:
                            yield {
                                "event": "status",
                                "data": json.dumps({
                                    "message": f"Retrying batch {batch_number + 1}",
                                    "progress": len(all_transactions),
                                    "total": total_needed,
                                    "status": "retrying"
                                })
                            }

                        batch_number += 1
                        await asyncio.sleep(1)

                    except Exception as e:
                        print(f"Error in batch {batch_number}: {str(e)}")
                        yield {
                            "event": "error",
                            "data": json.dumps({
                                "message": f"Error in batch {batch_number + 1}: {str(e)}",
                                "status": "error"
                            })
                        }

                # Final status
                yield {
                    "event": "complete",
                    "data": json.dumps({
                        "message": f"Successfully generated {len(all_transactions)} transactions",
                        "transactions": all_transactions,
                        "status": "complete"
                    })
                }

            except Exception as e:
                print(f"Generation failed: {str(e)}")
                yield {
                    "event": "error",
                    "data": json.dumps({
                        "message": f"Transaction generation failed: {str(e)}",
                        "status": "error"
                    })
                }

        return EventSourceResponse(event_generator())
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)