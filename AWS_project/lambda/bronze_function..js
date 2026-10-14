// I wrote this logic in lambda, this servers as a replication for your viewing. 

import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3Client = new S3Client({ region: process.env.AWS_REGION });

export const handler = async (event) => {

    const corsHeaders = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
      };

    try {
        const body = JSON.parse(event.body || "{}");
        if(Object.keys(body).length === 0) {return JSON.stringify({error: "The body object was empty..."})};
        const bucketName = "csvcollection"; 
        
        // If you want it inside a 'bronze' folder, prepend it to the file key
        const fileName = body.fileName || `${Date.now()}.json`; 
        const fileKey = `bronze/${fileName}`; 
        
        const contentType = body.contentType || 'application/json'; 

        const command = new PutObjectCommand({
            Bucket: bucketName,
            Key: fileKey,
            ContentType: contentType, 
        });  

        const presignedUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 });

        return {
            statusCode: 200, 
            headers: corsHeaders,
            body: JSON.stringify({ uploadURL: presignedUrl, fileKey: fileKey }),
        };

    } catch (error) {
        return {
            statusCode: 500, 
            headers: corsHeaders,
            body: JSON.stringify({ error: error.message }),
        };
    }
};
