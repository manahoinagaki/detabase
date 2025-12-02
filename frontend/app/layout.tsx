// \frontend\Alternative_data_frontend\frontend\app\layout.tsx

import type { Metadata } from "next";
import "./globals.css";
import "leaflet/dist/leaflet.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Manufacturing Dashboard",
    description: "Nowcasting dashboard for manufacturing index"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="ja">
            <body className={inter.className}>{children}</body>
        </html>
    );
}

