
import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import {
  Box,
  Button,
  TextField,
  Typography,
  Avatar,
  CircularProgress,
  IconButton,
  Paper,
  Select,
  MenuItem
} from "@mui/material";
import {
  Send as SendIcon,
  AccountCircle as AccountCircleIcon,
  SmartToy as SmartToyIcon,
  AttachMoney as AttachMoneyIcon,
  Warning as RiskLevelIcon
} from "@mui/icons-material";

const API_BASE_URL = "http://10.3.33.203:5001";

const FinancialChatBot = () => {
  // === State ===
  const [estimatedSavings, setEstimatedSavings] = useState(() => {
    const saved = localStorage.getItem("estimatedSavings");
    return saved ? parseFloat(saved) : 5000;
  });
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [riskLevels, setRiskLevels] = useState([]);
  const [riskPreference, setRiskPreference] = useState("medium");

  const messagesEndRef = useRef(null);

 
  // === Persist savings ===
  useEffect(() => {
    localStorage.setItem("estimatedSavings", estimatedSavings.toString());
  }, [estimatedSavings]);

  // === Fetch risk levels ===
  const fetchSupported = useCallback(async () => {
    try {
      const resp = await axios.get(`${API_BASE_URL}/api/stocks`);
      setRiskLevels(resp.data.risk_levels);
    } catch {
      setRiskLevels(["low", "medium", "high"]);
    }
  }, []);

  // === Init chat ===
  useEffect(() => {
    const welcome = {
      type: "bot",
      text: `Welcome! You have $${estimatedSavings.toLocaleString()} to invest. Ask about any stocks or request recommendations.`,
      time: new Date().toLocaleTimeString(),
    };
    setMessages([welcome]);
    fetchSupported();
  }, [estimatedSavings, fetchSupported]);

  // === Auto‑scroll ===
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // === Update profile on backend ===
  const updateInvestmentProfile = async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/update_profile`, {
        amount: estimatedSavings,
        risk: riskPreference,
      });
      localStorage.setItem("riskPreference", riskPreference);
    } catch (e) {
      console.error("Failed to update profile:", e);
    }
  };

  // === Analyze a single stock / query ===
  const analyzeStock = async (text) => {
    try {
      const tickerMatch = text.match(/\b[A-Z]{2,4}\b/);
      const params = { amount: estimatedSavings };
      if (tickerMatch) params.ticker = tickerMatch[0].toUpperCase();
      else params.ticker = text;  // Use 'ticker' instead of 'query'

      const { data } = await axios.get(`${API_BASE_URL}/api/analyze`, { params });

      let out = `📊 ${data.ticker} (${data.trend.toUpperCase()} trend | Technical Confidence: ${(data.technical_confidence*100).toFixed(0)}%)\n\n`;
      out += `💰 Current Price: $${data.current_price}\n🔹 Open: $${data.open_price}\n🔹 High: $${data.high_price}\n🔹 Low: $${data.low_price}\n`;
      out += `🔹 Previous Close: $${data.previous_close}\n🔹 Volume: ${data.volume.toLocaleString()}\n\n`;
      out += `📊 Technical Indicators:\n🔸 10‑Day SMA: $${data.sma_10}\n🔸 PE Ratio: ${data.pe_ratio || "N/A"}\n`;
      out += `🔸 Dividend Yield: ${(data.dividend_yield * 100).toFixed(2)}%\n🔸 Price Change: ${data.price_change_pct}%\n🔸 Volatility: ${data.volatility_pct}%\n\n`;
      out += `💵 With $${estimatedSavings.toLocaleString()}, you could buy ~${data.shares_possible} shares.\n\n`;
      out += `📰 News Sentiment: ${data.overall_news_sentiment}\n${data.news}\n\n`;

      // — NEW: detailed headline sentiments —
      if (data.detailed_sentiments?.length) {
        out += `📝 Sentiment Details:\n`;
        data.detailed_sentiments.forEach((it, i) => {
          out += `${i + 1}. ${it.label} (${it.score}) — ${it.headline}\n`;
        });
        out += `\n`;
      }

      // NEW: Display Financial Sentiment and Content
      out += `📊 Financial Statement Sentiment: ${data.financial_statements_sentiment || "N/A"}\n`;
      out += `📝 Financial Statement Content: ${data.financial_statements_content || "No financial data available"}\n`;

      out += `🤖 Analyst's Insight:\n${data.analysis}\n`;
      return out;
    } catch (e) {
      return `❌ Couldn't analyze. ${e.response?.data?.error || e.message}`;
    }
  };

  // === Recommendations endpoint ===
  const getRecommendations = async () => {
    try {
      const resp = await axios.get(`${API_BASE_URL}/api/recommend`, {
        params: { amount: estimatedSavings, risk: riskPreference }
      });
      if (resp.data.status === 'no_recommendations') {
        return "🔍 No strong recommendations found. Try adjusting your risk level.";
      }
      let out = `📊 ${riskPreference.toUpperCase()} RISK PORTFOLIO ($${estimatedSavings.toLocaleString()})\n\n`;
      resp.data.recommendations.forEach((item, i) => {
        out += `🏷️ ${i + 1}. ${item.ticker} (${item.sector?.toUpperCase() || "GENERAL"})\n`;
        out += `   💵 Price: $${item.price.toFixed(2)}\n`;
        out += `   ${item.trend === 'up' ? '📈' : '⚠️'} Trend: ${item.trend.toUpperCase()}\n`;
        out += `   ✅ Confidence: ${(item.confidence * 100).toFixed(1)}%\n`;
        out += `   🛒 Buy: ${item.shares} shares ($${(item.shares * item.price).toFixed(2)})\n\n`;
      });
      out += "💡 Suggested Allocation:\n";
      resp.data.allocation_plan.forEach(a => {
        out += `- ${a.ticker}: ${a.percentage}% ($${a.amount.toFixed(2)} → ${a.shares} shares)\n`;
      });
      return out;
    } catch (e) {
      return `⚠️ Backend Error: ${e.response?.data?.error || e.message}`;
    }
  };

  // === Handle user sending a message ===
  const handleSubmit = async () => {
    if (!input.trim()) return;
    setMessages(m => [...m, { type: "user", text: input, time: new Date().toLocaleTimeString() }]);
    setInput("");
    setLoading(true);

    let reply;
    if (/recommend|suggestion/i.test(input)) {
      reply = await getRecommendations();
    } else {
      reply = await analyzeStock(input);
    }

    setMessages(m => [...m, { type: "bot", text: reply, time: new Date().toLocaleTimeString() }]);
    setLoading(false);
  };

  // === Render one chat bubble ===
  const renderMessage = (msg) => (
    <Box key={msg.time + msg.text} sx={{
      display: "flex", alignItems: "center", gap: 1, mb: 2,
      flexDirection: msg.type === "user" ? "row-reverse" : "row"
    }}>
      <Avatar sx={{
        bgcolor: msg.type === "user" ? "primary.main" : "secondary.main",
        width: 32, height: 32
      }}>
        {msg.type === "user" ? <AccountCircleIcon /> : <SmartToyIcon />}
      </Avatar>
      <Paper elevation={3} sx={{
        p: 2, maxWidth: "75%",
        bgcolor: msg.type === "user" ? "primary.main" : "background.paper",
        color: msg.type === "user" ? "primary.contrastText" : "text.primary",
        borderRadius: msg.type === "user" ? "18px 18px 0 18px" : "18px 18px 18px 0"
      }}>
        <Typography whiteSpace="pre-line">{msg.text}</Typography>
        <Typography variant="caption" sx={{
          display: "block", textAlign: "right", opacity: 0.7,
          color: msg.type === "user" ? "primary.contrastText" : "text.secondary"
        }}>
          {msg.time}
        </Typography>
      </Paper>
    </Box>
  );

  // === Clear the chat ===
  const clearChat = () => {
    setMessages([{
      type: "bot",
      text: `Chat cleared. You have $${estimatedSavings.toLocaleString()} to invest.`,
      time: new Date().toLocaleTimeString()
    }]);
  };

  // === Render ===
  return (
    <Box sx={{
      width: "100%",
      background: "radial-gradient(circle, #888888, #444444, #1c1c1c)",
      color: "white",
      minHeight: "100vh"
    }}>
      

      {/* Header */}
      <Box sx={{ pt: "80px", textAlign: "center" }}>
        <Typography
          variant="h3"
          sx={{
            fontWeight: "bold",
            mb: 2,
            fontSize: { xs: "2rem", md: "3rem" },
            display: "inline-flex",
            alignItems: "center",
            gap: "12px"
          }}
        >
          <span style={{ fontSize: "2.5rem" }}>📈</span>
          Investment Assistant
        </Typography>
      </Box>

      {/* Chat Window */}
      <Box sx={{
        pt: "20px",
        maxWidth: "800px",
        mx: "auto",
        px: 2,
        display: "flex",
        flexDirection: "column",
        minHeight: "calc(100vh - 180px)"
      }}>
        <Box sx={{
          flexGrow: 1,
          overflowY: "auto",
          mb: 2,
          backgroundColor: "#2f2f2f",
          borderRadius: "16px",
          p: 3,
          boxShadow: "0px 6px 16px rgba(0,0,0,0.3)"
        }}>
          {messages.map(renderMessage)}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" gap={1}>
              <CircularProgress size={20} sx={{ color: "#ccc" }} />
              <Typography sx={{ fontStyle: "italic", color: "#ccc" }}>
                Analyzing...
              </Typography>
            </Box>
          )}
          <div ref={messagesEndRef} />
        </Box>

        {/* Controls */}
        <Box sx={{ display: "flex", gap: 2, mb: 2, position: "relative" }}>
          {/* Amount */}
          <Box sx={{
            flexGrow: 1,
            position: "relative",
            border: "1px solid #555",
            borderRadius: "4px",
            backgroundColor: "#2a2a2a"
          }}>
            <Typography sx={{
              position: "absolute",
              top: "-10px",
              left: "10px",
              backgroundColor: "#1e1e1e",
              px: 1,
              fontSize: "0.75rem",
              fontWeight: "bold",
              color: "white"
            }}>
              Amount
            </Typography>
            <TextField
              type="number"
              value={estimatedSavings}
              onChange={e => setEstimatedSavings(parseFloat(e.target.value) || 0)}
              InputProps={{
                startAdornment: <AttachMoneyIcon sx={{ color: "white", mr: 1 }} />,
                sx: { color: "white", "& .MuiOutlinedInput-notchedOutline": { borderColor: "transparent" } }
              }}
              sx={{ width: "100%" }}
            />
          </Box>

          {/* Risk */}
          <Box sx={{
            flexGrow: 1,
            position: "relative",
            border: "1px solid #555",
            borderRadius: "4px",
            backgroundColor: "#2a2a2a"
          }}>
            <Typography sx={{
              position: "absolute",
              top: "-10px",
              left: "10px",
              backgroundColor: "#1e1e1e",
              px: 1,
              fontSize: "0.75rem",
              fontWeight: "bold",
              color: "white"
            }}>
              Risk
            </Typography>
            <Select
              value={riskPreference}
              onChange={e => setRiskPreference(e.target.value)}
              sx={{
                width: "100%",
                color: "white",
                "& .MuiSelect-icon": { color: "white" },
                "& .MuiOutlinedInput-notchedOutline": { borderColor: "transparent" }
              }}
            >
              {riskLevels.map(r => (
                <MenuItem key={r} value={r}>
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                    <RiskLevelIcon fontSize="small" />
                    {r.charAt(0).toUpperCase() + r.slice(1)}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </Box>

          {/* Update Button */}
          <Button
            variant="contained"
            onClick={updateInvestmentProfile}
            sx={{
              height: "56px",
              alignSelf: "center",
              backgroundColor: "#00e3ae",
              color: "#1e1e1e",
              fontWeight: "bold",
              "&:hover": { backgroundColor: "#00c49a" }
            }}
          >
            Update
          </Button>
        </Box>

        {/* Input + Send */}
        <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
          <TextField
            fullWidth
            placeholder="Ask about stocks or request recommendations..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleSubmit()}
            disabled={loading}
            sx={{
              backgroundColor: "#1e1e1e",
              borderRadius: "10px",
              "& .MuiOutlinedInput-notchedOutline": { borderColor: "#444" },
              input: { color: "white" }
            }}
          />
          <IconButton
            onClick={handleSubmit}
            disabled={loading || !input.trim()}
            sx={{
              backgroundColor: "#1976d2",
              "&:hover": { backgroundColor: "#1565c0" },
              color: "white",
              ml: 1
            }}
          >
            <SendIcon />
          </IconButton>
        </Box>

        {/* Clear Chat */}
        <Button
          variant="outlined"
          onClick={clearChat}
          sx={{
            alignSelf: "center",
            mt: 2, mb: 3,
            color: "#fff",
            borderColor: "#ccc",
            "&:hover": { borderColor: "#f50057", backgroundColor: "#ff1744" }
          }}
        >
          Clear Chat
        </Button>
      </Box>
    </Box>
  );
};

export default FinancialChatBot;
