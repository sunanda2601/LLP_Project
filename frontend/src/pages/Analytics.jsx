import { useEffect, useState }
    from "react";

import api from "../services/api";

export default function Analytics() {
    const [data, setData] = useState(null);

    useEffect(() => {
        api.get("/analytics")
        .then(res => {
            setData(res.data);
        });
    }, []);

    if (!data)
        return <div>Loading...</div>;

    return (
        <div>
            <h2>Learning Analytics</h2>
            <p>Goal: {data.goal}</p>
            <p>Progress: {data.progress}</p>
            <p>Words Learned: {data.words_learned}</p>
        </div>
    );
}
