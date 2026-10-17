const mammoth = require("mammoth");
const fs = require("fs");
const path = require("path");

const parentDir = "C:\\Users\\rodri\\Documents\\MadLab";

function findFiles(dir, filesList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      findFiles(fullPath, filesList);
    } else if (file.endsWith(".docx")) {
      filesList.push(fullPath);
    }
  }
  return filesList;
}

const allDocs = findFiles(parentDir);

async function extractAll() {
  const extractedData = {};
  for (const docPath of allDocs) {
    try {
      const result = await mammoth.extractRawText({path: docPath});
      const basename = path.basename(docPath);
      extractedData[basename] = result.value.substring(0, 1500); // just getting the start to understand the structure
      console.log(`Extracted: ${basename}`);
    } catch (e) {
      console.error(`Error with ${docPath}:`, e.message);
    }
  }
  fs.writeFileSync("all_docs_summary.json", JSON.stringify(extractedData, null, 2));
}

extractAll();
