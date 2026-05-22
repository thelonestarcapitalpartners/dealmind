'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Load user's deals from API
    setLoading(false);
  }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">DealMind</h1>
          <button className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            New Deal
          </button>
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-semibold text-gray-800">My Deals</h2>
          
          {loading ? (
            <div className="mt-4">Loading deals...</div>
          ) : deals.length === 0 ? (
            <div className="mt-4 rounded-lg border-2 border-dashed border-gray-300 bg-white p-8 text-center">
              <p className="text-gray-600">No deals yet</p>
              <p className="mt-2 text-sm text-gray-500">
                Create your first deal to get started
              </p>
            </div>
          ) : (
            <div className="mt-4 grid gap-4">
              {/* TODO: Render deal cards */}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
