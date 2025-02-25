const { exec } = require("child_process");
const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios"); // Import axios for making API requests

const app = express();
const PORT = 3000;
const PYTHON_API_URL = "http://127.0.0.1:8000/process_invoice"; // Local Python server URL

app.use(bodyParser.json());

// Webhook route
app.post("/webhook/invoice", async (req, res) => {
  const invoiceData = req.body;
  console.log("📩 Received invoice webhook:", invoiceData);

  try {
    // Call the Python parser API
    const response = await axios.post(PYTHON_API_URL, invoiceData);
    console.log("✅ Python parser response:", response.data);

    res.status(200).json({
      status: "success",
      message: "Invoice processed",
      python_response: response.data,
    });
  } catch (error) {
    console.error("❌ Error calling Python API:", error);
    res.status(500).json({ status: "error", message: "Python processing failed" });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Webhook server running at http://localhost:${PORT}`);
});
// Automatically start webhook server when app.py runs
if (require.main === module) {
    console.log("🚀 Starting Node.js Webhook Server...");
    exec("node src/webhook.js", (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Webhook server failed: ${error.message}`);
            return;
        }
        if (stderr) console.error(`🚀 Webhook started with warnings: ${stderr}`);
        console.log(stdout);
    });
}
