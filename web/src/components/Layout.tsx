import React from "react";
import DashboardHeader from "@/components/DashboardHeader";
import dashboardBg from "@/assets/dashboard-bg.jpg";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-background relative">
      {/* Background */}
      <div 
        className="absolute inset-0 opacity-5 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${dashboardBg})` }}
      />
      
      {/* Content */}
      <div className="relative z-10">
        <DashboardHeader />
        <main className="px-6 py-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;