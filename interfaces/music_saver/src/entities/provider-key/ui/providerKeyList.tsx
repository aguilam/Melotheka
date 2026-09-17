import { createSignal, For, Show } from "solid-js";
import NewProviderKeyForm from "./newProviderKeyForm";
import { Button } from "~/components/ui/button";
import { createProviderKeyQuery } from "../api/queries";
import ProviderKeyCard from "./providerKeyCard";

const ProviderKeyList = () => {
  const [isCreating, setIsCreating] = createSignal(false);

  const providerKeys = () => providerKeyQuery.data;

  const providerKeyQuery = createProviderKeyQuery();

  return (
    <div>
      <div class="flex justify-between items-center mb-3">
        <p>Providers keys</p>
        <Button onClick={() => setIsCreating(!isCreating())}>+</Button>
      </div>
      <div class=" flex flex-col gap-2">
        <For each={providerKeys()}>{(key) => <ProviderKeyCard providerKey={key} />}</For>
        <Show when={isCreating() == true}>
          <NewProviderKeyForm setIsChange={setIsCreating} />
        </Show>
      </div>
    </div>
  );
};
export default ProviderKeyList;
