import { For } from "solid-js";
import { Button } from "~/components/ui/button";
import ApiKeyCard from "./apiKeyCard";
import { createApiKeyMutation, createApiKeyQuery } from "../api/queries";

const ApiKeyList = () => {
  const apiKeyQuery = createApiKeyQuery();
  const apiKeys = () => apiKeyQuery.data;
  const createApiMutation = createApiKeyMutation();
  const handleCreateApiKey = () => {
    createApiMutation.mutate();
  };
  return (
    <div>
      <div class="flex justify-between items-center mb-3">
        <p>API keys</p>
        <Button onClick={handleCreateApiKey}>+</Button>
      </div>
      <div class=" flex flex-col gap-2">
        <For each={apiKeys()}>{(key) => <ApiKeyCard apiKey={key} />}</For>
      </div>
    </div>
  );
};
export default ApiKeyList;
