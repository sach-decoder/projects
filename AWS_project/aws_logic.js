export async function sendToBucket(file, fileName) {
  const response = await fetch("https://3izz6bysx8.execute-api.eu-north-1.amazonaws.com/corsEnabled/bronze_function", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fileName: fileName, contentType: file.type })
  });

  if (!response.ok) {
    throw new Error("Could not get upload URL");
  }

  const { uploadURL } = await response.json();

  const uploadResponse = await fetch(uploadURL, {
    method: "PUT",
    headers: { "Content-Type": "text/csv" },
    body: file
  });

  if (!uploadResponse.ok) {
    throw new Error("Upload error occured.");
  }
}