import { For } from "solid-js";
import { Button } from "~/components/ui/button";
import SyncCard from "./syncCard";
import { createPostSyncMutation, createSyncsQuery } from "../api/queries";

const SyncList = () => {
  const syncsQuery = createSyncsQuery();
  const syncs = () => syncsQuery.data;
  const createSyncMutation = createPostSyncMutation();

  const handleStartSync = () => {
    createSyncMutation.mutate();
  };
  return (
    <div>
      <div class=" flex gap-2 items-center">
        <p>Sync</p>
        <Button onClick={handleStartSync}>Start sync</Button>
      </div>
      <For each={syncs()}>{(sync) => <SyncCard sync={sync} />}</For>
    </div>
  );
};

export default SyncList;
