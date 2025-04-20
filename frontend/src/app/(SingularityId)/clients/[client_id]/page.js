import { ClientForm } from "./form";

const ClientPage = async ({ params }) => {

    const { client_id } = await params;

    
    return (
        <ClientForm client_id = {client_id}/>
    );
};

export default ClientPage;
