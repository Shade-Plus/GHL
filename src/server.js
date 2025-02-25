const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Define folder paths
const GHL_FOLDER = "C:\\Users\\ryanc\\OneDrive\\Desktop\\GHL";
const LOG_FILE = path.join(GHL_FOLDER, "task_log.txt");

// Ensure the GHL folder exists
if (!fs.existsSync(GHL_FOLDER)) {
    fs.mkdirSync(GHL_FOLDER, { recursive: true });
}

// Function to log messages for debugging
function logMessage(message) {
    const timestamp = new Date().toISOString();
    fs.appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
}

// GoHighLevel API Key (Replace when expired)
const GHL_API_KEY = "pit-7e321aab-1830-4ad2-a1af-d83c7a5a4e1b";

// Function to fetch invoices using Puppeteer
async function fetchInvoicesWithBrowser() {
    logMessage("Launching Puppeteer browser...");
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    try {
        // Set API headers (mimicking a real browser session)
        await page.setExtraHTTPHeaders({
            "Authorization": `Bearer ${GHL_API_KEY}`,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "application/json"
        });

        // Navigate to the API endpoint
        logMessage("Navigating to GoHighLevel API...");
        await page.goto("https://rest.gohighlevel.com/v1/invoices", {
            waitUntil: 'networkidle2' // Wait for network activity to settle
        });

        // Extract API response as text
        const responseText = await page.evaluate(() => document.body.innerText);

        // Log and save the response
        logMessage("Received API response.");
        console.log("API Response:", responseText);

        // Save response to a file
        const fileName = `invoices_${new Date().toISOString().replace(/:/g, "-")}.txt`;
        const filePath = path.join(GHL_FOLDER, fileName);
        fs.writeFileSync(filePath, responseText);
        logMessage(`Invoice data saved to: ${filePath}`);

        await browser.close();
        return responseText;
    } catch (error) {
        logMessage(`Error fetching invoices: ${error.message}`);
        console.error("Error:", error);
        await browser.close();
        return null;
    }
}

// Run the function
fetchInvoicesWithBrowser();
