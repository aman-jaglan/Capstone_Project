import React, { useEffect, useState } from "react";
import { Box, Typography, Button, Grid, Collapse, Card,CardContent, TextField, Divider } from "@mui/material";
import { Link } from "react-router-dom";
import { useSpring, animated } from "@react-spring/web";
import { Fade } from "react-awesome-reveal";
import axios from "axios";


const BudgetOptimization = () => {
  const heroAnimation = useSpring({
    from: { opacity: 0, transform: "translateY(-20px)" },
    to: { opacity: 1, transform: "translateY(0)" },
    config: { duration: 1000 },
  });

  const [userDetails, setUserDetails] = useState({
    income: "",
    
  });
  useEffect(() => {
    const appLaunched = sessionStorage.getItem("appLaunched");
    if (!appLaunched) {
      localStorage.removeItem("savedOptimizations");
      sessionStorage.setItem("appLaunched", "true");
    }
  }, []);
  

  const [categorySpending, setCategorySpending] = useState({});
  const [suggestions, setSuggestions] = useState("");
  const [budget, setBudget] = useState(0);
  const [chatbotResponse, setChatbotResponse] = useState(() => {
    return localStorage.getItem("chatbotResponse") || "";
  });
  const [isChatting, setIsChatting] = useState(false);
  const [error, setError] = useState(null);
  const [expandedCard, setExpandedCard] = useState(null); 
  const [isWarning, setIsWarning] = useState(false);
  const [estimatedSavings, setEstimatedSavings] = useState(null);
  const [savingsRange, setSavingsRange] = useState(""); 
    
  const extractEstimatedSavings = (responseText) => {
    const lines = responseText.split("\n");
    const dollarRegex = /\$?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)/g;
  
    for (let line of lines) {
      // NEW ➔ Capture 'Total estimated monthly savings'
      if (/total\s+estimated\s+monthly\s+savings/i.test(line)) {
        const matches = [...line.matchAll(dollarRegex)].map(m =>
          parseFloat(m[1].replace(/,/g, ""))
        );
        if (matches.length === 2) {
          const average = (matches[0] + matches[1]) / 2;
          return {
            average,
            rangeText: `$${matches[0].toFixed(0)} - $${matches[1].toFixed(0)}`
          };
        } else if (matches.length === 1) {
          return {
            average: matches[0],
            rangeText: `$${matches[0].toFixed(0)}`
          };
        }
      }
    }
  
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const isOverallLine = /overall\s+(estimated\s+)?monthly\s+savings/i.test(line) ||
                            /overall\s+estimated/i.test(line);
  
      if (isOverallLine) {
        const sameLineMatches = [...line.matchAll(dollarRegex)].map(m =>
          parseFloat(m[1].replace(/,/g, ""))
        );
        if (sameLineMatches.length === 2) {
          const average = (sameLineMatches[0] + sameLineMatches[1]) / 2;
          return {
            average,
            rangeText: `$${sameLineMatches[0].toFixed(0)} - $${sameLineMatches[1].toFixed(0)}`
          };
        } else if (sameLineMatches.length === 1) {
          return {
            average: sameLineMatches[0],
            rangeText: `$${sameLineMatches[0].toFixed(0)}`
          };
        }
  
        for (let j = i + 1; j <= i + 5 && j < lines.length; j++) {
          const nextLine = lines[j];
          if (/per\s+year/i.test(nextLine)) continue;
  
          const matches = [...nextLine.matchAll(dollarRegex)].map(m =>
            parseFloat(m[1].replace(/,/g, ""))
          );
          if (matches.length === 2) {
            const average = (matches[0] + matches[1]) / 2;
            return {
              average,
              rangeText: `$${matches[0].toFixed(0)} - $${matches[1].toFixed(0)}`
            };
          } else if (matches.length === 1) {
            return {
              average: matches[0],
              rangeText: `$${matches[0].toFixed(0)}`
            };
          }
        }
      }
    }
  
    for (let line of lines) {
      if (/save/i.test(line) && /per\s+month/i.test(line) && !/per\s+year/i.test(line)) {
        const matches = [...line.matchAll(dollarRegex)].map(m =>
          parseFloat(m[1].replace(/,/g, ""))
        );
        if (matches.length === 2) {
          const average = (matches[0] + matches[1]) / 2;
          return {
            average,
            rangeText: `$${matches[0].toFixed(0)} - $${matches[1].toFixed(0)}`
          };
        } else if (matches.length === 1) {
          return {
            average: matches[0],
            rangeText: `$${matches[0].toFixed(0)}`
          };
        }
      }
    }
  
    return { average: 0, rangeText: "$0" };
  };
  
  
  useEffect(() => {
    setChatbotResponse("");
    setEstimatedSavings(null);
    setSavingsRange("");
  
    const savedSpending = localStorage.getItem("categorizedSpending");
    if (savedSpending) {
      const parsedSpending = JSON.parse(savedSpending);
      setCategorySpending(parsedSpending);
      const totalBudget = Object.values(parsedSpending).reduce((sum, amount) => sum + amount, 0);
      setBudget(totalBudget);
    }
  
    if (!sessionStorage.getItem("appLaunched")) {
      localStorage.removeItem("savedOptimizations");
      sessionStorage.setItem("appLaunched", "true");
    }
  }, []);
  
  

  const optimizeBudget = () => {
    console.log("Optimizing budget...");
    
    if (!categorySpending || Object.keys(categorySpending).length === 0) {
      setSuggestions("No spending data available. Please categorize transactions first.");
      return;
    }
  
    let advice = "\n";
    let flaggedCategories = [];
  
    const income = parseFloat(userDetails.income);

    const totalSpending = Object.values(categorySpending).reduce((sum, amount) => sum + amount, 0);

    if (income < totalSpending) {
      setIsWarning(true); 
      setChatbotResponse(""); 
      setSuggestions(
        "🚫 Your total monthly spending exceeds your stated income. Please review and adjust your income value before proceeding with optimization."
      );
      return;
    }
    setIsWarning(false); 

  
    let adjustedNeedsThreshold = income * 0.50;
    let adjustedWantsThreshold = income * 0.30;
    let adjustedSavingsThreshold = income * 0.20;
  
    let totalNeeds = 0;
    let totalWants = 0;
    let totalSavings = 0;
  
    Object.entries(categorySpending).forEach(([category, amount]) => {
      if (category === "Food" || category === "Housing" || category === "Transportation" || category === "Utilities" || category === "Insurance") {
        totalNeeds += amount;
        if (totalNeeds > adjustedNeedsThreshold) {
          advice += `⚠️ You are spending too much on Needs: ${category} (${amount.toFixed(2)}). Consider cutting back to stay within the 50% budget.\n`;
          flaggedCategories.push(category);
        } else {
          advice += `✅ Spending on ${category} (${amount.toFixed(2)}) is under control within your "Needs" category.\n`;
        }
      } else if (category === "Entertainment" || category === "Dining Out" || category === "Shopping" || category === "Travel") {
        totalWants += amount;
        if (totalWants > adjustedWantsThreshold) {
          advice += `⚠️ You are spending too much on Wants: ${category} (${amount.toFixed(2)}). Consider cutting back to stay within the 30% budget.\n`;
          flaggedCategories.push(category);
        } else {
          advice += `✅ Spending on ${category} (${amount.toFixed(2)}) is under control within your "Wants" category.\n`;
        }
      } else {
        totalSavings += amount;
        if (totalSavings < adjustedSavingsThreshold) {
          advice += `⚠️ You should increase your savings. Current savings amount: ${amount.toFixed(2)}. Aim for at least 20% of your income in savings.\n`;
          flaggedCategories.push(category);
        } else {
          advice += `✅ You are saving well with ${category} (${amount.toFixed(2)}) within your "Savings" category.\n`;
        }
      }
    });
  
    if (flaggedCategories.length === 0) {
      advice += "\n🎉 Congratulations! You are on track with your spending and savings. Keep up the good work!";
    } else {
      advice += "\n🔔 Consider adjusting your budget to better align with the 50/30/20 rule. By cutting back on non-essential spending and boosting savings, you can achieve a more balanced budget.";
    }
    
    setSuggestions(advice);  
    getChatbotResponse(flaggedCategories);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserDetails({ ...userDetails, [name]: value });
  };

  const validateInputs = () => {
    const income = parseFloat(userDetails.income);
   
    if (!/^\d+(\.\d{1,2})?$/.test(userDetails.income) || income <= 0) {
      setError("Income must be a valid number greater than 0.");
      return false;
    }
  
    setError(null);
    return true;
  };
  

  const getChatbotResponse = (flaggedCategories) => {
    if (!validateInputs()) return;
  
  
    let flaggedCategoriesText = flaggedCategories.length > 0
      ? `The user is spending too much in these categories: ${flaggedCategories.join(", ")}. Provide recommendations on reducing expenses in these areas.`
      : "The user's spending is generally balanced.";
  
    const requestData = {
      model: "llama3-8b-8192",
      messages: [
        {
          role: "user",
          content: `User details: Income: ${userDetails.income},
    Monthly Spending Breakdown: ${JSON.stringify(categorySpending)} ${flaggedCategoriesText}.

    Based on the user's demographics and spending, provide personalized budget optimization suggestions.

    - In grocery recommendations, include different store names based on affordability and general popularity.

    - Suggest specific action steps for groceries, shopping, travel, and other overspending areas. Suggest estimated monthly savings based on the user's profile.

    - Ensure every response is unique and uses varied store names and examples.

    -- Adjust your focus on savings and spending based on the user's income level.
  
  - Give **Overall Monthly Savings** at the end everytime.`,
        },
      ],
      temperature: 0.1,
    };
  
    axios.post(
      "https://api.groq.com/openai/v1/chat/completions",
      requestData,
      {
        headers: {
          Authorization: `Bearer YOUR_API_KEY`,
          "Content-Type": "application/json",
        },
      }
    )
    .then((response) => {
      if (response.data.choices && response.data.choices.length > 0) {
        const text = response.data.choices[0].message.content.trim();
        setChatbotResponse(text);
    
        const { average, rangeText } = extractEstimatedSavings(text);
        if (!isNaN(average)) {
          setEstimatedSavings(average);
          setSavingsRange(rangeText);
          localStorage.setItem("estimatedSavings", average.toString()); 
          localStorage.setItem("chatbotResponse", text); 
        }
      } else {
        setChatbotResponse("No response from the model.");
      }
    })
    
    .catch((error) => {
      console.error("Error interacting with Groq Llama model:", error);
      setError("Sorry, there was an error. Please try again.");
    })
    .finally(() => {
      setIsChatting(false);
    });
  };
    
  const toggleCard = (category) => {
    if (expandedCard === category) {
      setExpandedCard(null); 
    } else {
      setExpandedCard(category); 
    }
  };
   
  const categorySuggestions = {
    Food: {
      under: "You're managing your food expenses well! Meal planning is paying off.",
      over: "Food costs are high. Try meal prepping and using store loyalty programs to cut back.",
    },
    Housing: {
      under: "Great job keeping housing costs stable. That's a solid foundation!",
      over: "Housing costs seem high. Consider negotiating rent or refinancing if possible.",
    },
    Shopping: {
      under: "Your shopping habits are within budget. Keep tracking discretionary spending.",
      over: "Too much on shopping? Try setting a fixed monthly limit or use cashback apps.",
    },
    Travel: {
      under: "You're managing travel costs well. Smart travel planning!",
      over: "Travel is eating into your budget. Try off-season bookings or loyalty points.",
    },
    Utilities: {
      under: "Utility spending is under control. Efficient energy usage helps!",
      over: "Utility bills are high. Consider turning off unused appliances or adjusting thermostat use.",
    },
    Insurance: {
      under: "Insurance expenses are optimized. Great job!",
      over: "Check if bundling policies or switching providers could save you on insurance.",
    },
    Entertainment: {
      under: "You are keeping entertainment costs low — that is a smart leisure balance.",
      over: "Entertainment is over budget. Look for free events or subscription sharing options.",
    },
    DiningOut: {
      under: "Dining out costs are modest. Nice job balancing convenience and savings.",
      over: "Cut back on eating out — try cooking more meals at home to save.",
    },
    Transportation: {
      under: "Transportation costs are efficient. Great use of transit or fuel management!",
      over: "Review transport costs. Carpooling or public transit could help.",
    },
    default: {
      under: "This category is well managed.",
      over: "You may want to review spending in this category.",
    }
  };

  const generateSummaryCards = () => {
    return Object.entries(categorySpending).map(([category, amount]) => {
      const isUnderControl = amount <= (parseFloat(userDetails.income) * 0.1);
      const cardTitle = `${category} - $${amount.toFixed(2)} (${isUnderControl ? "Under Control" : "Over Budget"})`;
      const cardColor = isUnderControl ? "#4CAF50" : "#FF9800";
      const iconColor = "#ffffff";
  
      const suggestion =
        categorySuggestions[category]?.[isUnderControl ? "under" : "over"] ||
        categorySuggestions["default"][isUnderControl ? "under" : "over"];
  
      return (
        <Grid item xs={12} md={6} key={category}>
          <Card
            sx={{
              backgroundColor: cardColor,
              color: "white",
              marginBottom: "20px",
              borderRadius: "10px",
              boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.2)",
              '&:hover': {
                boxShadow: "0px 6px 18px rgba(0, 0, 0, 0.3)",
                transform: "scale(1.02)",
                transition: "all 0.3s ease-in-out",
              },
            }}
          >
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", cursor: "pointer" }} onClick={() => toggleCard(category)}>
                <Box sx={{ marginRight: "10px" }}>
                  <Typography sx={{ fontSize: "24px", color: iconColor }}>
                    {isUnderControl ? "✔️" : "⚠️"}
                  </Typography>
                </Box>
                <Typography sx={{ fontWeight: "bold", marginLeft: "8px" }} variant="h6">
                  {cardTitle}
                </Typography>
              </Box>
              <Collapse in={expandedCard === category} timeout="auto" unmountOnExit>
                <Typography variant="body2" sx={{ mt: 2, fontSize: "14px" }}>
                  {suggestion}
                </Typography>
              </Collapse>
            </CardContent>
          </Card>
        </Grid>
      );
    });
  };

 

  return (
    <Box
      sx={{
        width: "100%",
        background: "radial-gradient(circle, #0f0f0f, #1c1c1c, #2f2f2f)",
        color: "white",
        minHeight: "100vh",
      }}
    >

      <Box sx={{ pt: "100px", textAlign: "center" }}>
        <animated.div style={heroAnimation}>
        <Typography
            variant="h3"
            sx={{
              fontFamily: "'Segoe UI Emoji', 'Noto Color Emoji', sans-serif",
              fontWeight: "bold",
              mb: 4,
              letterSpacing: "1.5px",
              fontSize: { xs: "2rem", md: "3rem" },
              textAlign: "center",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: "12px",
              overflow: "visible", 
            }}
          >
            <span style={{ fontSize: "2.5rem", lineHeight: 1 }}>💸</span>
            <span style={{ position: "relative", display: "inline-block" }}>
            {/* Shadow Layer */}
            <span style={{
              position: "absolute",
              top: 0,
              left: 0,
              color: "#ffffff",
              opacity: 0.2,
              filter: "blur(2px)",
              zIndex: 0,
            }}>
              Budget Optimization
            </span>

            {/* Gradient Text Layer */}
            <span style={{
              background: "linear-gradient(135deg, rgb(255, 255, 255), rgb(140, 161, 211), rgb(116, 136, 173), rgb(255, 255, 255))",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              display: "inline-block",
              lineHeight: "1.4",
              animation: "gradientFlow 6s ease infinite",
              backgroundSize: "600% 600%",
              position: "relative",
              zIndex: 1,
            }}>
              Budget Optimization
            </span>
          </span>
          </Typography>

        </animated.div>

        <Fade triggerOnce>
          <Grid container spacing={3} justifyContent="center">
            <Grid item xs={12} md={6}>
              <Card sx={{ backgroundColor: "#2f2f2f", color: "white" }}>
                <CardContent>
                <Typography
                  variant="h5"
                  sx={{
                    mb: 4,
                    fontWeight: "medium",
                    fontSize: { xs: "1.25rem", md: "1.5rem" },
                    color: "#white",
                    textShadow: "0 0 8px rgba(255, 255, 255, 0.4)",
                    textAlign: "center",
                    letterSpacing: "0.5px",
                    
                  }}
                >
                  📋 Provide your income to get a customized budget
                </Typography>
                  {[
                    { label: "Income", key: "income" },
                  ].map((field, index) => (
                    <TextField
                      label={field.label}
                      variant="outlined"
                      fullWidth
                      margin="normal"
                      name={field.key}
                      value={userDetails[field.key]}
                      onChange={handleInputChange}
                      InputLabelProps={{
                        sx: { color: "#bbb", fontWeight: "bold", fontSize: "1rem" },
                      }}
                      InputProps={{
                        sx: {
                          color: "white",
                          backgroundColor: "#1e1e1e",
                          borderRadius: "12px",
                          padding: "10px 14px",
                          "& .MuiOutlinedInput-notchedOutline": {
                            borderColor: "#444",
                          },
                          "&:hover .MuiOutlinedInput-notchedOutline": {
                            borderColor: "#888",
                          },
                          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                            borderColor: "#1976d2", 
                          },
                        },
                      }}
                      sx={{ mt: 2 }}
                    />

                  ))}
                  <Button variant="contained" color="primary" 
                  sx={{ 
                    mt: 2,
                    background: "linear-gradient(135deg, #4caf50, #388e3c)",
                    boxShadow: "0 4px 10px rgba(76, 175, 80, 0.3)",
                    borderRadius: "10px",
                    fontWeight: "bold",
                    padding: "10px 16px",
                    transition: "all 0.3s ease-in-out", 
                    '&:hover': {
                      background: "linear-gradient(135deg, #43e97b, #38f9d7)",
                      boxShadow: "0 8px 20px rgba(67, 233, 123, 0.4)",
                      transform: "scale(1.03)",
                    }}} 
                  onClick={optimizeBudget} disabled={isChatting} 
                  >
                    {isChatting ? "Processing..." : "Optimize Budget"}
                  </Button>
                  <br></br>
                  {isWarning && !chatbotResponse && (
                    <Typography
                      sx={{
                        mt: 3,
                        px: 3,
                        py: 2,
                        backgroundColor: "#ff4444",
                        borderRadius: "10px",
                        color: "#fff",
                        textAlign: "center",
                        fontWeight: "bold",
                        boxShadow: "0 0 10px rgba(255, 68, 68, 0.4)",
                      }}
                    >
                      {suggestions}
                    </Typography> 
                    
                  )}
                  <br></br>

                  {error && <Typography color="error">{error}</Typography>}
                  {chatbotResponse && (
                  <Box
                    sx={{
                      padding: 5,
                      borderRadius: "10px",
                      background: "radial-gradient(circle, #888888, #444444, #1c1c1c)",
                      backgroundSize: "200% 200%",
                      animation: "gradientFlow 15s ease infinite",
                      position: "relative",            
                      boxShadow: "0px 6px 12px rgba(0, 0, 0, 0.3)",
                      marginBottom: "2rem",
                      textAlign: "center",  
                    }}
                  >
                    <Typography
                      variant="h5"
                      sx={{
                        fontWeight: "bold",
                        color: "#FFD700", 
                        mb: 3,  
                      }}
                    >
                      💡 Chatbot Suggestions:
                    </Typography>
                    <Divider sx={{backgroundColor: "#FFD700" }} /> {/* More spacing between title and content */}
                    
                    <Box
                      sx={{
                        fontFamily: "'Roboto', sans-serif",
                        fontSize: "1rem",
                        color: "#FFFFFF",  
                        lineHeight: "1.8",
                        padding: "2rem",
                        borderRadius: "8px",
                        textAlign: "justify",  
                        display: "block",  
                        whiteSpace: "pre-line",  
                        wordWrap: "break-word", 
                      }}
                    >
                      {/* Format titles and bold categories differently */}
                      <div
                  dangerouslySetInnerHTML={{
                    __html: chatbotResponse
                      
                      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")  
                      }}
                    />

                   </Box>
                </Box>
                )}
                  <Grid container spacing={3} justifyContent="center">
                    {suggestions && (generateSummaryCards())}
                  </Grid>
                  {estimatedSavings !== null && (
                  <Typography
                    variant="h5"
                    sx={{
                      mt: 3,
                      px: 4,
                      py: 3,
                      borderRadius: "12px",
                      fontWeight: "bold",
                      textAlign: "center",
                      boxShadow: "0px 8px 16px rgba(0, 0, 0, 0.2)",
                      width: "fit-content",
                      mx: "auto",
                      fontSize: "1.4rem",
                      background: "linear-gradient(45deg, #6A1B9A, #00897B, #1E88E5)",
                      backgroundSize: "300% 300%",
                      animation: "gradientFlow 6s ease infinite",
                      color: "white",
                      letterSpacing: "0.5px",
                    }}
                  >
                    Estimated Monthly Savings: 
                    <span style={{ color: "#FFD700", fontSize: "1.6rem" }}>
                      {estimatedSavings.toFixed(2)}
                    </span>
                    {savingsRange && (
                      <span style={{ color: "#CCCCCC", fontSize: "0.95rem" }}>
                        {" "}({savingsRange})
                      </span>
                    )}
                  </Typography>
                )}


                  <Typography
                    variant="h5"
                    sx={{
                      mt: 5,
                      px: 3,
                      py: 2,
                      borderRadius: "12px",
                      color: "white",
                      fontWeight: "bold",
                      textAlign: "center",
                      boxShadow: "0px 4px 12px rgba(0, 0, 0, 0.3)",
                      width: "fit-content",
                      mx: "auto",
                      fontSize: "1.25rem",
                      background: "radial-gradient(circle, #888888, #444444, #1c1c1c)",
                      backgroundSize: "400% 400%",
                      animation: "gradientFlow 6s ease infinite",
                    }}
                  >
                    💰 Your Current Spending: <span style={{ color: "#FFD700" }}>${budget.toFixed(2)}</span>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Fade>
      </Box>

      <br></br>
      <br></br>
      <br></br>

      <Box sx={{ textAlign: "center", mt: 4 }}>

          <Button
      component={Link}
      to="/investment"
      state={{ estimatedSavings }}
      variant="contained"
      color="secondary"
      sx={{ padding: "10px 20px" }}
    >
      🧠 Get Financial Advice
    </Button>
    </Box>

      <Box
        component="footer"
        sx={{
          width: "100%",
          padding: "1rem",
          color: "white",
          textAlign: "center",
        }}
      >
        <Typography variant="body2">© {new Date().getFullYear()} Financial Assistant. All rights reserved.</Typography>
      </Box>
    </Box>
  );
};

export default BudgetOptimization;
