import { Component, Show } from "solid-js";
import ConfigInput from "~/entities/server/ui/configInput";
import { user } from "~/shared/store/user";
import ProviderKeyList from "~/entities/provider-key/ui/providerKeyList";
import ApiKeyList from "~/entities/api-key/ui/apiKeyList";
import SyncList from "~/features/sync/ui/syncList";
const SettingsPage: Component = () => {
  return (
    <div class=" flex flex-col gap-5 m-2">
      <p>Settings</p>
      <ApiKeyList />
      <ProviderKeyList />

      <Show when={user.isAdmin}>
        <SyncList />
        <ConfigInput />
      </Show>
    </div>
  );
};
export default SettingsPage;
