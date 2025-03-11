import "./globals.css";
import { NextUIProvider } from "@nextui-org/react";

export const metadata = {
  title: "Auth",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <NextUIProvider>
          <div className="flex flex-col h-screen dark text-foreground bg-background">
            {children}
          </div>
        </NextUIProvider>
      </body>
    </html>
  );
}
