import { exchangeAuthCode } from '@/utils/actions';
import { redirect } from 'next/navigation';

export default async function authorize({ searchParams }) {
    // Extract URI parameters
    let params = await searchParams;

    if (params.code) {
        exchangeAuthCode(params.code)
    }
    
    // Redirect the user to the home page
    redirect('/');
}