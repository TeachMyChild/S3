import { S3Client, ListObjectsV2Command } from "@aws-sdk/client-s3";

// Create an S3 client with default credentials
const s3Client = new S3Client({ region: "YOUR_REGION" });

// Define the parameters for listing objects in the bucket
const params = {
  Bucket: "YOUR_BUCKET_NAME",
};

// Function to list objects in the S3 bucket
async function listObjects() {
  try {
    const data = await s3Client.send(new ListObjectsV2Command(params));
    if (data.Contents) {
      console.log("Objects in the bucket:");
      data.Contents.forEach((object) => {
        console.log(object.Key);
      });
    } else {
      console.log("No objects found in the bucket.");
    }
  } catch (err) {
    console.error("Error listing objects:", err);
  }
}

// Call the function to list objects
listObjects();
