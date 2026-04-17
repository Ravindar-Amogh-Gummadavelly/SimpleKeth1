import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/predict/:path*", destination: "http://127.0.0.1:8001/predict/:path*" },
      { source: "/api/predict", destination: "http://127.0.0.1:8001/predict" },
      { source: "/api/recommend/:path*", destination: "http://127.0.0.1:8002/recommend/:path*" },
      { source: "/api/recommend", destination: "http://127.0.0.1:8002/recommend" },
      { source: "/api/notify/:path*", destination: "http://127.0.0.1:8003/notify/:path*" },
      { source: "/api/notify", destination: "http://127.0.0.1:8003/notify" },
      { source: "/api/farmers/:path*", destination: "http://127.0.0.1:8004/farmers/:path*" },
      { source: "/api/farmers", destination: "http://127.0.0.1:8004/farmers" },
      { source: "/api/mandis", destination: "http://127.0.0.1:8004/mandis" },
      { source: "/api/crops", destination: "http://127.0.0.1:8004/crops" },
      // Catch-all fallback
      { source: "/api/:path*", destination: "http://127.0.0.1:8000/:path*" },
    ];
  },
};

export default nextConfig;
