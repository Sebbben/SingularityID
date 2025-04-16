import { ClientList } from "./clientList";

const DashboardPage = () => {
    return (
        <div className="flex items-center justify-center h-full">
            <div className="max-w-4xl w-full p-4">
                <h1 className="text-2xl font-bold text-center mb-6 text-gray-800 dark:text-gray-200">
                    Dashboard
                </h1>
                <ClientList />
            </div>
        </div>
    );
};

export default DashboardPage;