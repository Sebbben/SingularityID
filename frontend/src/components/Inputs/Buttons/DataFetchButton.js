import API from "@/utils/api"
import { Button } from "@nextui-org/react"

export function DataFetchButton(props) {
    const fetchData = () => {
        API.GET(props.url, props.args).then(([status, data]) => {
            props.callback(data);
        })
    }

    return (
        <Button color="primary" onPress={fetchData}>
            {props.text}
        </Button>
    )
}