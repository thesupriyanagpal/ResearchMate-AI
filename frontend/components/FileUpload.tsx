"use client";

import { uploadFile } from '@/lib/api';
import { CheckCircle, Loader2, Upload } from 'lucide-react';
import React, { useState } from 'react';

export default function FileUpload({ onUploadComplete }: { onUploadComplete: (data: any) => void }) {
    const [isUploading, setIsUploading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setIsUploading(true);
            try {
                const data = await uploadFile(file);
                setUploadStatus('success');
                onUploadComplete(data);
            } catch (error) {
                console.error("Upload failed", error);
                setUploadStatus('error');
            } finally {
                setIsUploading(false);
            }
        }
    };

    return (
        <div className="p-6 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors text-center">
            <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center gap-2">
                {isUploading ? (
                    <Loader2 className="w-10 h-10 text-blue-500 animate-spin" />
                ) : uploadStatus === 'success' ? (
                    <CheckCircle className="w-10 h-10 text-green-500" />
                ) : (
                    <Upload className="w-10 h-10 text-gray-400" />
                )}
                <span className="text-sm font-medium text-gray-600">
                    {isUploading ? "Processing PDF..." : uploadStatus === 'success' ? "Upload Complete" : "Click to Upload Research Paper (PDF)"}
                </span>
            </label>
        </div>
    );
}
