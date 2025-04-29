import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  Grid,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tabs,
  Tab,
  IconButton,
  InputAdornment,
  CircularProgress,
  Alert,
  Avatar,
  Container,
  LinearProgress,
  TablePagination
} from '@mui/material';
import {
  Upload as UploadIcon,
  CloudUpload as CloudUploadIcon,
  Person as PersonIcon,
  AttachMoney as AttachMoneyIcon,
  Home as HomeIcon,
  LocationOn as LocationIcon,
  Male as MaleIcon,
  Female as FemaleIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import Papa from 'papaparse';

const Profile = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState('upload');
  const [userData, setUserData] = useState({
    age: '',
    gender: '',
    householdSize: '',
    annualIncome: '',
    zipcode: '',
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [transactions, setTransactions] = useState(() => {
    const savedTransactions = localStorage.getItem('synthetic_transactions');
    return savedTransactions ? JSON.parse(savedTransactions) : [];
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [file, setFile] = useState(null);
  const [showMappingStep, setShowMappingStep] = useState(false);
  const [mappedTransactions, setMappedTransactions] = useState([]);
  const [generationStatus, setGenerationStatus] = useState('');
  const [generationProgress, setGenerationProgress] = useState(0);
  const [totalTransactions, setTotalTransactions] = useState(0);
  const [currentMerchants, setCurrentMerchants] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedTransactions, setGeneratedTransactions] = useState([]);
  const [showTransactionTable, setShowTransactionTable] = useState(false);
  
  const API_URL = "https://credgeai.cloud.arc.gwu.edu/groq/generate";  // Updated API endpoint

  const handleUpload = async () => {
    if (!file) return setError("Please select a file first.");
    if (file.type !== "application/pdf" && file.type !== "text/csv") {
      setError("Unsupported file type. Please upload a PDF or CSV only.");
      return;
    }
  
    setLoading(true);
    try {
      let transactions = [];
  
      if (file.type === "text/csv") {
        const csvText = await file.text();
        transactions = await parseCSV(csvText);
      } else if (file.type === "application/pdf") {
        const pdfText = await parsePDF(file);
        transactions = await parseCSV(pdfText);
      }
  
      const formattedTransactions = transactions.map((t) => ({
        Category: t.Category || "Unknown",
        Amount: parseFloat(t.Amount) || 0,
        "Transaction Date": new Date(t["Transaction Date"]).toLocaleDateString(),
      }));
  
      // Save formatted transactions to localStorage
      localStorage.setItem('transactions', JSON.stringify(formattedTransactions));
  
      // Optional: also prepare categorized spending for Pie Chart
      const categoryTotals = formattedTransactions.reduce((acc, transaction) => {
        acc[transaction.Category] = (acc[transaction.Category] || 0) + transaction.Amount;
        return acc;
      }, {});
      localStorage.setItem('categorizedSpending', JSON.stringify(categoryTotals));
  
      // You can navigate to Dashboard or show a success message if you want
      navigate('/dashboard');
  
    } catch (err) {
      console.error(err);
      setError("Failed to upload or parse file.");
    } finally {
      setLoading(false);
    }
  };
  

  // Switch between "Upload Statement" and "Generate Data" modes
  const handleModeChange = (newMode) => {
    setMode(newMode);
    setTransactions([]);
    setError('');
  };

  // Handle text input changes (age, gender, etc.)
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData((prev) => ({ ...prev, [name]: value }));
  };

  // Store the selected file in local state
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setFile(e.target.files[0]);
    setError('');
  };

  // Helper to parse CSV text
  const parseCSV = (csvData) => {
    return new Promise((resolve, reject) => {
      Papa.parse(csvData, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          // Check for parsing errors
          if (result.errors && result.errors.length > 0) {
            reject(result.errors[0]);
          } else {
            resolve(result.data);
          }
        },
        error: (error) => reject(error),
      });
    });
  };

  // Upload PDF to server and get text returned
  const parsePDF = async (pdfFile) => {
    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      const response = await fetch("https://credgeai.cloud.arc.gwu.edu/transaction/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Error uploading PDF.");

      // Expecting the server to return raw CSV text after parsing the PDF
      return await response.text();
    } catch (error) {
      throw error;
    }
  };

  // Add this category mapping function at the top of your Profile component
  const mapToStandardCategories = (transactions) => {
    const categoryMappings = {
        // Food & Grocery
        "groceries": "Food",
        "deli_prepared_foods": "Food",
        "bakery": "Food",
        "packaged_foods": "Food",
        "vending_snacks": "Food",
        "ice_cream": "Food",
        "seafood_market": "Food",
        "food_truck": "Food",
        "restaurant_dining": "Food",
        "catering_services": "Food",
        // Original categories
        "Grocery Store": "Food",
        "Delicatessen": "Food",
        "Bakery": "Food",
        "Food Products": "Food",
        "Food Vending Machine": "Food",
        "Ice Cream Manufacture": "Food",
        "Marine Food Retail": "Food",
        "Mobile Delicatessen": "Food",
        "Restaurant": "Food",
        "Caterers": "Food",

        // Transportation
        "gas_station": "Transportation",
        "car_rental": "Transportation",
        "car_wash": "Transportation",
        "towing_services": "Transportation",
        "towing_company": "Transportation",
        "vehicle_storage": "Transportation",
        "driving_lessons": "Transportation",
        // Original categories
        "Gasoline Dealer": "Transportation",
        "Auto Rental": "Transportation",
        "Auto Wash": "Transportation",
        "Tow Truck": "Transportation",
        "Tow Truck Business": "Transportation",
        "Tow Truck Storage Lot": "Transportation",
        "Driving School": "Transportation",

        // Entertainment
        "movie_theater": "Entertainment",
        "event_venue": "Entertainment",
        "live_theater": "Entertainment",
        "bowling": "Entertainment",
        "pool_hall": "Entertainment",
        "skating_rink": "Entertainment",
        "sports_events": "Entertainment",
        "special_events": "Entertainment",
        // Original categories
        "Motion Picture Theatre": "Entertainment",
        "Public Hall": "Entertainment",
        "Theater (Live)": "Entertainment",
        "Bowling Alley": "Entertainment",
        "Billiard Parlor": "Entertainment",
        "Skating Rink": "Entertainment",
        "Athletic Exhibition": "Entertainment",
        "Special Events": "Entertainment",

        // Lodging
        "hotel_lodging": "Lodging",
        "motel_lodging": "Lodging",
        "bnb_lodging": "Lodging",
        "vacation_rental": "Lodging",
        "boarding_house": "Lodging",
        // Original categories
        "Hotel": "Lodging",
        "Inn And Motel": "Lodging",
        "Bed and Breakfast": "Lodging",
        "Vacation Rental": "Lodging",
        "Boarding House": "Lodging",

        // Personal Care
        "beauty_services": "Personal Care",
        "barber_services": "Personal Care",
        "beauty_booth": "Personal Care",
        "hair_braiding": "Personal Care",
        "electrolysis": "Personal Care",
        "skin_care": "Personal Care",
        "nail_salon": "Personal Care",
        "spa_services": "Personal Care",
        "massage_parlor": "Personal Care",
        // Original categories
        "Beauty Shop": "Personal Care",
        "Barber Shop": "Personal Care",
        "Beauty Booth": "Personal Care",
        "Beauty Shop Braiding": "Personal Care",
        "Beauty Shop Electrology": "Personal Care",
        "Beauty Shop Esthetics": "Personal Care",
        "Beauty Shop Nails": "Personal Care",
        "Health Spa": "Personal Care",
        "Massage Establishment": "Personal Care"
    };

    return transactions.map(transaction => {
        const originalCategory = transaction.merchant_details?.category || '';
        const merchantName = transaction.merchant_details?.name || '';
        
        // First try exact match from the original category
        let standardCategory = categoryMappings[originalCategory];

        // If no match found, try matching the mapped category (from transaction_synthesizer)
        if (!standardCategory && transaction.merchant_details?.mapped_category) {
            standardCategory = categoryMappings[transaction.merchant_details.mapped_category];
        }

        // If still no match, try keyword matching in merchant name
        if (!standardCategory) {
            const merchantNameLower = merchantName.toLowerCase();
            if (merchantNameLower.includes('restaurant') || merchantNameLower.includes('food') || 
                merchantNameLower.includes('cafe') || merchantNameLower.includes('grocery')) {
                standardCategory = 'Food';
            } else if (merchantNameLower.includes('beauty') || merchantNameLower.includes('salon') || 
                      merchantNameLower.includes('spa')) {
                standardCategory = 'Personal Care';
            } else if (merchantNameLower.includes('hotel') || merchantNameLower.includes('motel') || 
                      merchantNameLower.includes('inn')) {
                standardCategory = 'Lodging';
            } else if (merchantNameLower.includes('theater') || merchantNameLower.includes('cinema') || 
                      merchantNameLower.includes('entertainment')) {
                standardCategory = 'Entertainment';
            } else if (merchantNameLower.includes('auto') || merchantNameLower.includes('car') || 
                      merchantNameLower.includes('gas')) {
                standardCategory = 'Transportation';
            }
        }

        // Default to 'Other' if no category match found
        standardCategory = standardCategory || 'Other';

        return {
            Category: standardCategory,
            Amount: parseFloat(transaction.amount),
            "Transaction Date": new Date(transaction.timestamp).toLocaleDateString(),
            Description: merchantName,
            OriginalCategory: originalCategory
        };
    });
  };

  // Add this function to help debug category mappings
  const logCategoryDistribution = (transactions) => {
    const distribution = transactions.reduce((acc, t) => {
      acc[t.Category] = (acc[t.Category] || 0) + 1;
      return acc;
    }, {});
    
    console.log('Category Distribution:', distribution);
    return distribution;
  };

  // Add a function to clear transactions
  const handleClearTransactions = () => {
    if (window.confirm('Are you sure you want to clear existing transactions? This will allow you to generate new ones.')) {
      setTransactions([]);
      localStorage.removeItem('synthetic_transactions');
      localStorage.removeItem('transactions'); // Clear mapped transactions
      localStorage.removeItem('categorizedSpending');
      setUserData({
        age: '',
        gender: '',
        householdSize: '',
        annualIncome: '',
        zipcode: '',
      });
    }
  };

  // Modify the handleSubmit function
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (transactions.length > 0) {
      setError("Please clear existing transactions before generating new ones.");
      return;
    }

    const { age, gender, householdSize, annualIncome, zipcode } = userData;
    if (!age || !gender || !householdSize || !annualIncome || !zipcode) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Origin': window.location.origin
        },
        credentials: 'include',
        body: JSON.stringify({
          age: Number(age),
          gender,
          household_size: Number(householdSize),
          income: Number(annualIncome),
          zipcode
        }),
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      const newTransactions = Array.isArray(data) ? data : (data.transactions || []);
      
      // Save to localStorage and state
      localStorage.setItem('synthetic_transactions', JSON.stringify(newTransactions));
      setTransactions(newTransactions);
      setError('');
    } catch (err) {
      setError(err.message);
      console.error("Error generating data:", err);
    } finally {
      setLoading(false);
    }
  };

  // Add a new function to handle the "Next Step" action
  const handleNextStep = () => {
    const mappedTxns = mapToStandardCategories(transactions);
    setMappedTransactions(mappedTxns);
    localStorage.setItem('transactions', JSON.stringify(mappedTxns));
    navigate('/dashboard');
  };

  // Reset form and clear transactions
  const handleReset = () => {
    setUserData({
      age: '',
      gender: '',
      householdSize: '',
      annualIncome: '',
      zipcode: '',
    });
    setTransactions([]);
    setError('');
  };

  const handleMapAndNavigate = () => {
    try {
      setLoading(true);
      
      // Map the transactions
      const mappedTransactions = mapToStandardCategories(transactions);
      
      // Log category distribution
      console.log('Original Transactions:', transactions);
      console.log('Mapped Transactions:', mappedTransactions);
      const distribution = logCategoryDistribution(mappedTransactions);
      
      // Alert if too many "Other" categories
      const otherCount = distribution['Other'] || 0;
      const totalCount = mappedTransactions.length;
      const otherPercentage = (otherCount / totalCount) * 100;
      
      if (otherPercentage > 20) {
        console.warn(`Warning: ${otherPercentage.toFixed(1)}% of transactions mapped to 'Other' category`);
      }
      
      // Save to localStorage
      localStorage.setItem('transactions', JSON.stringify(mappedTransactions));
      
      // Calculate and save category totals
      const categoryTotals = mappedTransactions.reduce((acc, transaction) => {
        acc[transaction.Category] = (acc[transaction.Category] || 0) + transaction.Amount;
        return acc;
      }, {});
      localStorage.setItem('categorizedSpending', JSON.stringify(categoryTotals));
      
      // Navigate to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Error mapping transactions:', error);
      setError('Failed to process transactions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateSyntheticTransactions = async () => {
    // Validate input data
    const requestData = {
        age: parseInt(userData.age),
        gender: userData.gender,
        household_size: parseInt(userData.householdSize),
        income: parseFloat(userData.annualIncome),
        zipcode: userData.zipcode
    };

    if (!requestData.age || !requestData.gender || !requestData.household_size || 
        !requestData.income || !requestData.zipcode) {
        setError('Please fill in all fields');
        return;
    }

    setIsGenerating(true);
    setGeneratedTransactions([]);
    setGenerationProgress(0);
    setGenerationStatus('Initializing connection...');
    setError('');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',  // Changed to POST
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
                'Origin': window.location.origin
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { value, done } = await reader.read();
            
            if (done) {
                console.log("Stream complete");
                break;
            }

            const chunk = decoder.decode(value);
            buffer += chunk;
            
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (line.trim() && line.startsWith('data:')) {
                    try {
                        const rawData = line.slice(5).trim();
                        if (!rawData) continue;

                        const jsonData = JSON.parse(rawData);

                        // Update UI states
                        if (jsonData.message) setGenerationStatus(jsonData.message);
                        if (jsonData.total) setTotalTransactions(jsonData.total);
                        if (jsonData.progress !== undefined) setGenerationProgress(jsonData.progress);
                        if (jsonData.merchants) setCurrentMerchants(jsonData.merchants);
                        if (jsonData.transactions) {
                            setGeneratedTransactions(prev => [...prev, ...jsonData.transactions]);
                        }

                        if (jsonData.status === 'complete') {
                            setGenerationStatus('Generation complete!');
                            if (jsonData.transactions) {
                                const mappedTransactions = mapToStandardCategories(jsonData.transactions);
                                setGeneratedTransactions(jsonData.transactions);
                                localStorage.setItem('transactions', JSON.stringify(mappedTransactions));
                                
                                const categoryTotals = mappedTransactions.reduce((acc, transaction) => {
                                    acc[transaction.Category] = (acc[transaction.Category] || 0) + transaction.Amount;
                                    return acc;
                                }, {});
                                localStorage.setItem('categorizedSpending', JSON.stringify(categoryTotals));
                            }
                            setIsGenerating(false);
                            setShowTransactionTable(true);
                            return;
                        }
                    } catch (e) {
                        console.error('Error processing SSE data:', e);
                        continue;
                    }
                }
            }
        }
    } catch (error) {
        console.error('Generation failed:', error);
        setError(`Failed to generate transactions: ${error.message}`);
    } finally {
        setIsGenerating(false);
    }
  };

  // Update the GenerationProgress component
  const GenerationProgress = () => {
    if (!isGenerating && !generatedTransactions.length) return null;

    return (
        <Card sx={{
            mt: 3,
            p: 3,
            background: 'rgba(26, 26, 26, 0.8)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '20px',
            boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
            color: '#ffffff'
        }}>
            {/* Status Header */}
            <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="h6">
                    Generation Status
                </Typography>
                {isGenerating && (
                    <CircularProgress size={20} sx={{ color: '#00C49F' }} />
                )}
            </Box>

            {/* Status Message */}
            <Typography sx={{ 
                color: error ? '#ff6b6b' : '#00C49F', 
                mb: 2 
            }}>
                {error || generationStatus}
            </Typography>

            {/* Progress Bar */}
            {totalTransactions > 0 && (
                <Box sx={{ mb: 3 }}>
                    <LinearProgress
                        variant="determinate"
                        value={(generationProgress / totalTransactions) * 100}
                        sx={{
                            height: 8,
                            borderRadius: 4,
                            backgroundColor: 'rgba(255, 255, 255, 0.1)',
                            '& .MuiLinearProgress-bar': {
                                backgroundColor: '#00C49F'
                            }
                        }}
                    />
                    <Typography variant="body2" sx={{ mt: 1, color: '#b3b3b3' }}>
                        {generationProgress} of {totalTransactions} transactions
                    </Typography>
                </Box>
            )}

            {/* Generation Log */}
            <Box sx={{
                mt: 2,
                p: 2,
                backgroundColor: 'rgba(0, 0, 0, 0.3)',
                borderRadius: '10px',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                fontFamily: 'monospace',
                maxHeight: '400px',
                overflow: 'auto'
            }}>
                {/* Current Merchants */}
                {currentMerchants?.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                        <Typography sx={{ color: '#4CAF50', fontSize: '0.9rem' }}>
                            Processing Merchants:
                        </Typography>
                        {currentMerchants.map((merchant, idx) => (
                            <Typography key={idx} sx={{ 
                                color: '#b3b3b3', 
                                ml: 2, 
                                fontSize: '0.85rem' 
                            }}>
                                → {merchant}
                            </Typography>
                        ))}
                    </Box>
                )}

                {/* Latest Transactions */}
                {generatedTransactions?.length > 0 && (
                    <Box>
                        <Typography sx={{ color: '#4CAF50', fontSize: '0.9rem' }}>
                            Latest Transactions:
                        </Typography>
                        {generatedTransactions.slice(-5).map((tx, idx) => (
                            <Typography key={idx} sx={{ 
                                color: '#b3b3b3', 
                                ml: 2, 
                                fontSize: '0.85rem' 
                            }}>
                                → ${tx.amount.toFixed(2)} at {tx.merchant_details.name}
                            </Typography>
                        ))}
                    </Box>
                )}
            </Box>
        </Card>
    );
  };

  // Add this new component for the completion view
  const CompletionView = ({ transactions }) => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);

    const handleNavigateToDashboard = () => {
        navigate('/dashboard');
    };

    return (
        <Card sx={{
            mt: 3,
            p: 3,
            background: 'rgba(26, 26, 26, 0.8)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '20px',
            boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
            color: '#ffffff'
        }}>
            <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6">
                    Generated Transactions
                </Typography>
                <Button
                    variant="contained"
                    onClick={handleNavigateToDashboard}
                    sx={{
                        background: 'linear-gradient(45deg, #00C49F 30%, #00A3FF 90%)',
                        color: 'white',
                        '&:hover': {
                            background: 'linear-gradient(45deg, #00A3FF 30%, #00C49F 90%)',
                        }
                    }}
                >
                    View in Dashboard
                </Button>
            </Box>

            <TableContainer sx={{ 
                maxHeight: 440,
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
                borderRadius: '10px'
            }}>
                <Table stickyHeader>
                    <TableHead>
                        <TableRow>
                            <TableCell sx={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: '#ffffff' }}>
                                Date
                            </TableCell>
                            <TableCell sx={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: '#ffffff' }}>
                                Merchant
                            </TableCell>
                            <TableCell sx={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: '#ffffff' }}>
                                Original Category
                            </TableCell>
                            <TableCell sx={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: '#ffffff' }}>
                                Mapped Category
                            </TableCell>
                            <TableCell sx={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', color: '#ffffff' }}>
                                Amount
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {transactions
                            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                            .map((transaction, index) => {
                                const mappedCategory = mapToStandardCategories([transaction])[0].Category;
                                return (
                                    <TableRow key={index} hover>
                                        <TableCell sx={{ color: '#b3b3b3' }}>
                                            {new Date(transaction.timestamp).toLocaleDateString()}
                                        </TableCell>
                                        <TableCell sx={{ color: '#b3b3b3' }}>
                                            {transaction.merchant_details.name}
                                        </TableCell>
                                        <TableCell sx={{ color: '#b3b3b3' }}>
                                            {transaction.merchant_details.category}
                                        </TableCell>
                                        <TableCell sx={{ color: '#b3b3b3' }}>
                                            {mappedCategory}
                                        </TableCell>
                                        <TableCell sx={{ color: '#b3b3b3' }}>
                                            ${transaction.amount.toFixed(2)}
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                    </TableBody>
                </Table>
            </TableContainer>
            
            <TablePagination
                component="div"
                count={transactions.length}
                page={page}
                onPageChange={(event, newPage) => setPage(newPage)}
                rowsPerPage={rowsPerPage}
                onRowsPerPageChange={(event) => {
                    setRowsPerPage(parseInt(event.target.value, 10));
                    setPage(0);
                }}
                sx={{ color: '#ffffff' }}
            />
        </Card>
    );
  };

  return (
    <Box
      sx={{
        background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
        minHeight: '100vh',
        color: '#ffffff',
        py: 2,
        px: { xs: 2, md: 4 }
      }}
    >
      {/* Hero Section */}
      <Box
        sx={{
          minHeight: '30vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          px: { xs: 2, md: 4 },
          position: 'relative',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, transparent 70%)',
            pointerEvents: 'none',
          }
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ textAlign: 'center' }}>
            <Typography
              variant="h1"
              sx={{
                fontWeight: 'bold',
                color: '#ffffff',
                fontSize: { xs: '2.5rem', md: '3.5rem' },
                mb: 2,
                lineHeight: 1.2,
                textShadow: '0px 0px 10px rgba(255, 255, 255, 0.3)',
              }}
            >
              Financial Data Management
            </Typography>
            <Typography
              variant="h5"
              sx={{
                color: '#b3b3b3',
                mb: 2,
                lineHeight: 1.6,
                fontSize: { xs: '1.1rem', md: '1.3rem' },
              }}
            >
              Upload your financial statements or generate synthetic data to get started with personalized financial insights and recommendations.
            </Typography>
          </Box>
        </Container>
      </Box>

      {/* Main Content */}
      <Box sx={{ maxWidth: '1200px', mx: 'auto', mt: -4 }}>
        <Grid container spacing={3}>
          {/* Left Side - User Info */}
          <Grid item xs={12} md={4}>
            <Card 
              sx={{ 
                p: 2, 
                background: 'rgba(26, 26, 26, 0.8)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                height: '100%',
                boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)'
              }}
            >
              <Box sx={{ textAlign: 'center', mb: 2 }}>
                <Avatar
                  sx={{ 
                    width: 80, 
                    height: 80, 
                    mx: 'auto',
                    mb: 1,
                    background: 'linear-gradient(45deg, rgba(255, 255, 255, 0.9) 30%, rgba(255, 255, 255, 0.7) 90%)',
                    color: '#1a1a1a'
                  }}
                >
                  <PersonIcon sx={{ fontSize: 40 }} />
                </Avatar>
                <Typography variant="h6" sx={{ mb: 1, color: '#ffffff' }}>
                  User Profile
                </Typography>
                <Typography variant="body2" sx={{ color: '#b3b3b3' }}>
                  Manage your personal information
                </Typography>
              </Box>

              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                <TextField
                  fullWidth
                  label="Age"
                  name="age"
                  value={userData.age}
                  onChange={handleInputChange}
                  sx={{ mb: 2 }}
                  InputLabelProps={{ style: { color: '#ffffff' } }}
                  InputProps={{
                    style: { color: '#ffffff' },
                    startAdornment: (
                      <InputAdornment position="start">
                        <PersonIcon sx={{ color: '#b3b3b3' }} />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Gender"
                  name="gender"
                  value={userData.gender}
                  onChange={handleInputChange}
                  sx={{ mb: 2 }}
                  InputLabelProps={{ style: { color: '#ffffff' } }}
                  InputProps={{
                    style: { color: '#ffffff' },
                    startAdornment: (
                      <InputAdornment position="start">
                        {userData.gender === 'male' ? (
                          <MaleIcon sx={{ color: '#b3b3b3' }} />
                        ) : (
                          <FemaleIcon sx={{ color: '#b3b3b3' }} />
                        )}
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Household Size"
                  name="householdSize"
                  value={userData.householdSize}
                  onChange={handleInputChange}
                  sx={{ mb: 2 }}
                  InputLabelProps={{ style: { color: '#ffffff' } }}
                  InputProps={{
                    style: { color: '#ffffff' },
                    startAdornment: (
                      <InputAdornment position="start">
                        <HomeIcon sx={{ color: '#b3b3b3' }} />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Annual Income"
                  name="annualIncome"
                  value={userData.annualIncome}
                  onChange={handleInputChange}
                  sx={{ mb: 2 }}
                  InputLabelProps={{ style: { color: '#ffffff' } }}
                  InputProps={{
                    style: { color: '#ffffff' },
                    startAdornment: (
                      <InputAdornment position="start">
                        <AttachMoneyIcon sx={{ color: '#b3b3b3' }} />
                      </InputAdornment>
                    ),
                  }}
                />
                <TextField
                  fullWidth
                  label="Zipcode"
                  name="zipcode"
                  value={userData.zipcode}
                  onChange={handleInputChange}
                  InputLabelProps={{ style: { color: '#ffffff' } }}
                  InputProps={{
                    style: { color: '#ffffff' },
                    startAdornment: (
                      <InputAdornment position="start">
                        <LocationIcon sx={{ color: '#b3b3b3' }} />
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>
            </Card>
          </Grid>

          {/* Right Side - Data Management */}
          <Grid item xs={12} md={8}>
            <Card 
              sx={{ 
                p: 2, 
                background: 'rgba(26, 26, 26, 0.8)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.3)'
              }}
            >
              <Tabs
                value={mode}
                onChange={(e, newValue) => handleModeChange(newValue)}
                sx={{ 
                  mb: 3,
                  '& .MuiTab-root': {
                    color: '#b3b3b3',
                    '&.Mui-selected': {
                      color: '#ffffff',
                    },
                  },
                }}
              >
                <Tab 
                  value="upload" 
                  label="Upload Statement" 
                  icon={<UploadIcon />} 
                  iconPosition="start"
                />
                <Tab 
                  value="generate" 
                  label="Generate Data" 
                  icon={<CloudUploadIcon />} 
                  iconPosition="start"
                />
              </Tabs>

              {error && (
                <Alert severity="error" sx={{ mb: 3, color: '#ffffff' }}>
                  {error}
                </Alert>
              )}

              {mode === 'upload' ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <input
                    accept=".csv,.pdf"
                    style={{ display: 'none' }}
                    id="raised-button-file"
                    type="file"
                    onChange={handleFileChange}
                  />
                  
                  <label htmlFor="raised-button-file">
                    <Button
                                          variant="contained"
                                          component="span"
                                          sx={{
                                            background: "linear-gradient(45deg, rgba(255, 255, 255, 0.9) 30%, rgba(255, 255, 255, 0.7) 90%)",
                                            color: "#1a1a1a",
                                            padding: "10px 22px",
                                            borderRadius: "10px",
                                            fontWeight: "600",
                                            textTransform: "uppercase",
                                            boxShadow: "0 4px 12px rgba(255, 255, 255, 0.2)",
                                            "&:hover": {
                                              background: "linear-gradient(45deg, rgba(255, 255, 255, 0.7) 30%, rgba(255, 255, 255, 0.9) 90%)",
                                              boxShadow: "0 6px 16px rgba(255, 255, 255, 0.3)",
                                            },
                                          }}
                                        >
                                          📁 Choose File
                                        </Button>
                    <Button
                                        onClick={handleUpload}
                                        disabled={loading}
                                        sx={{
                                          background: "linear-gradient(45deg, rgba(255, 255, 255, 0.9) 30%, rgba(255, 255, 255, 0.7) 90%)",
                                          color: "#1a1a1a",
                                          padding: "10px 22px",
                                          borderRadius: "10px",
                                          fontWeight: "600",
                                          textTransform: "uppercase",
                                          boxShadow: "0 4px 12px rgba(255, 255, 255, 0.2)",
                                          "&:hover": {
                                            background: "linear-gradient(45deg, rgba(255, 255, 255, 0.7) 30%, rgba(255, 255, 255, 0.9) 90%)",
                                            boxShadow: "0 6px 16px rgba(255, 255, 255, 0.3)",
                                          },
                                        }}
                                      >
                                        {loading ? "Uploading..." : "Upload"}
                                      </Button>
                  </label>
                  {selectedFile && (
                    <Typography variant="body2" sx={{ mt: 2, color: '#b3b3b3' }}>
                      Selected: {selectedFile.name}
                    </Typography>
                  )}
                </Box>
              ) : (
                <Box>
                  <Box sx={{ display: "flex", justifyContent: "center", mb: 3 }}>
                    <Button
                      variant="contained"
                      onClick={generateSyntheticTransactions}
                      disabled={isGenerating}
                      startIcon={isGenerating ? <CircularProgress size={20} /> : <CloudUploadIcon />}
                      sx={{
                        background: "linear-gradient(45deg, rgba(255, 255, 255, 0.9) 30%, rgba(255, 255, 255, 0.7) 90%)",
                        color: "#1a1a1a",
                        boxShadow: "0 3px 5px 2px rgba(255, 255, 255, .2)",
                        "&:hover": {
                          background: "linear-gradient(45deg, rgba(255, 255, 255, 0.7) 30%, rgba(255, 255, 255, 0.9) 90%)",
                        },
                        "&.Mui-disabled": {
                          background: "rgba(255, 255, 255, 0.12)",
                        },
                      }}
                    >
                      {isGenerating ? 'Generating...' : 'Generate Data'}
                    </Button>
                  </Box>

                  {transactions.length > 0 ? (
                    <Box>
                      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="h6" sx={{ color: '#ffffff' }}>
                          Generated Transactions: {transactions.length}
                        </Typography>
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={handleClearTransactions}
                          sx={{
                            borderColor: 'rgba(255, 99, 71, 0.5)',
                            color: 'tomato',
                            '&:hover': {
                              borderColor: 'tomato',
                              backgroundColor: 'rgba(255, 99, 71, 0.1)',
                            },
                          }}
                        >
                          Clear & Generate New
                        </Button>
                      </Box>
                      
                      <TableContainer component={Paper} sx={{ 
                        background: "rgba(26, 26, 26, 0.8)",
                        backdropFilter: "blur(10px)",
                        borderRadius: "20px",
                        border: "1px solid rgba(255, 255, 255, 0.1)",
                        boxShadow: "0 8px 32px 0 rgba(0, 0, 0, 0.3)",
                        maxHeight: "500px",
                        overflow: "auto",
                      }}>
                        <Table>
                          <TableHead>
                            <TableRow>
                              <TableCell sx={{ color: "#ffffff", fontWeight: "bold" }}>Date</TableCell>
                              <TableCell sx={{ color: "#ffffff", fontWeight: "bold" }}>Merchant</TableCell>
                              <TableCell sx={{ color: "#ffffff", fontWeight: "bold" }}>Original Category</TableCell>
                              <TableCell sx={{ color: "#ffffff", fontWeight: "bold" }}>Mapped Category</TableCell>
                              <TableCell sx={{ color: "#ffffff", fontWeight: "bold" }}>Amount</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {transactions.map((transaction, index) => (
                              <TableRow key={index}>
                                <TableCell sx={{ color: "#b3b3b3" }}>
                                  {new Date(transaction.timestamp).toLocaleDateString()}
                                </TableCell>
                                <TableCell sx={{ color: "#b3b3b3" }}>
                                  {transaction.merchant_details?.name || 'Unknown'}
                                </TableCell>
                                <TableCell sx={{ color: "#b3b3b3" }}>
                                  {transaction.merchant_details?.category || 'Unknown'}
                                </TableCell>
                                <TableCell sx={{ color: "#b3b3b3" }}>
                                  {mapToStandardCategories([transaction])[0].Category}
                                </TableCell>
                                <TableCell sx={{ color: "#b3b3b3" }}>
                                  ${parseFloat(transaction.amount).toFixed(2)}
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>

                      {/* Next Step Button */}
                      <Box sx={{ mt: 4, textAlign: 'center' }}>
                        <Button
                          variant="contained"
                          onClick={handleMapAndNavigate}
                          sx={{
                            background: "linear-gradient(45deg, #00C49F 30%, #00A3FF 90%)",
                            color: "white",
                            px: 4,
                            py: 2,
                            fontSize: "1.1rem",
                            borderRadius: "999px",
                            boxShadow: "0 3px 5px 2px rgba(0, 196, 159, .3)",
                            "&:hover": {
                              background: "linear-gradient(45deg, #00A3FF 30%, #00C49F 90%)",
                              transform: "translateY(-2px)",
                              transition: "all 0.3s ease",
                            },
                          }}
                        >
                          View in Dashboard
                        </Button>
                      </Box>
                    </Box>
                  ) : (
                    <Box sx={{ 
                      display: "flex", 
                      flexDirection: "column", 
                      alignItems: "center", 
                      justifyContent: "center",
                      minHeight: "200px",
                      color: "#b3b3b3"
                    }}>
                      <CloudUploadIcon sx={{ fontSize: 48, mb: 2 }} />
                      <Typography variant="h6">No data generated yet</Typography>
                      <Typography variant="body2">Fill in your profile details and click "Generate Data"</Typography>
                    </Box>
                  )}
                </Box>
              )}
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Generation Progress Component */}
      <GenerationProgress />
      
      {/* Show completion view when generation is done */}
      {!isGenerating && showTransactionTable && generatedTransactions.length > 0 && (
          <CompletionView transactions={generatedTransactions} />
      )}
    </Box>
  );
};

export default Profile;
