export default function AgentStatus({ state }) {
    return (
        <div>
            {state === "IDLE" && "🟢 Idle"}
            {state === "PLANNING" && "🟡 Planning"}
            {state === "TOOL_EXECUTION" && "🔵 Executing"}
            {state === "COMPLETED" && "✅ Completed"}
        </div>
    );
}
