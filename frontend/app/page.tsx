"use client";

import ChatInterface from '@/components/ChatInterface';
import FileUpload from '@/components/FileUpload';
import { BarChart3, BookOpen, BrainCircuit, Code2, FileText } from 'lucide-react';
import React, { useState } from 'react';

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<any>(null);

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-blue-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <BrainCircuit className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
              ResearchMate AI
            </h1>
          </div>
          <nav className="flex items-center gap-6 text-sm font-medium text-gray-600">
            <a href="#" className="hover:text-blue-600 transition-colors">Dashboard</a>
            <a href="#" className="hover:text-blue-600 transition-colors">Documentation</a>
            <a href="#" className="hover:text-blue-600 transition-colors">Settings</a>
          </nav>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Sidebar / Context Panel */}
        <div className="lg:col-span-4 space-y-6">
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-blue-500" />
              Research Context
            </h2>
            <FileUpload onUploadComplete={setUploadedFile} />

            {uploadedFile && (
              <div className="mt-6 p-4 bg-blue-50 rounded-xl border border-blue-100">
                <h3 className="font-medium text-blue-900 mb-1">Active Document</h3>
                <p className="text-sm text-blue-700 truncate">{uploadedFile.filename}</p>
                <div className="mt-3 flex gap-2 flex-wrap">
                  <span className="px-2 py-1 bg-white rounded-md text-xs font-medium text-blue-600 border border-blue-100">
                    {uploadedFile.text_length} chars
                  </span>
                  <span className="px-2 py-1 bg-white rounded-md text-xs font-medium text-green-600 border border-green-100">
                    Indexed
                  </span>
                </div>
              </div>
            )}
          </section>

          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-semibold mb-4">Capabilities</h2>
            <div className="space-y-3">
              <CapabilityItem icon={<FileText className="w-4 h-4" />} title="Summarization & Extraction" />
              <CapabilityItem icon={<BrainCircuit className="w-4 h-4" />} title="Insight Generation" />
              <CapabilityItem icon={<BarChart3 className="w-4 h-4" />} title="Comparison & Dashboards" />
              <CapabilityItem icon={<Code2 className="w-4 h-4" />} title="Python Code Generation" />
            </div>
          </section>
        </div>

        {/* Main Chat Area */}
        <div className="lg:col-span-8">
          <ChatInterface />
        </div>
      </div>
    </main>
  );
}

function CapabilityItem({ icon, title }: { icon: React.ReactNode, title: string }) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-default">
      <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center text-gray-600">
        {icon}
      </div>
      <span className="text-sm font-medium text-gray-700">{title}</span>
    </div>
  );
}
