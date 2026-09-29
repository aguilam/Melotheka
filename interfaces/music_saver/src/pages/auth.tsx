import { Navigate } from "@solidjs/router";
import { Component, Show } from "solid-js";
import AuthForm from "~/features/auth/ui/authForm";
import { user } from "~/shared/store/user";

const AuthPage: Component = () => {
  return (
    <Show when={!user.id} fallback={<Navigate href="/" />}>
      <AuthForm />
    </Show>
  );
};
export default AuthPage;
