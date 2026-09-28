import ky from "ky";
import { refreshAuth } from "~/features/auth";
import { setUser } from "../store/user";

export const API_URL = "/api/";
const api = ky.create({
  prefix: API_URL,
  credentials: "include",
});

export const client = api.extend({
  hooks: {
    afterResponse: [
      async ({ request, options, response }) => {
        const url = new URL(request.url);

        if (
          response.status !== 401 ||
          url.pathname.includes("/auth/refresh") ||
          url.pathname.includes("/auth/login") ||
          url.pathname.includes("/auth/register")
        ) {
          return response;
        }

        const refreshed = await refreshAuth();
        if (!refreshed) {
          setUser({
            id: NaN,
            username: "",
            isAdmin: false,
          });
          return response;
        }

        return api(request, options);
      },
    ],
  },
  parseJson: (text) => {
    return JSON.parse(text, (_, value) => {
      if (value && value.coverId != null) {
        value.coverUri = `${API_URL}covers/${value.coverId}`;
      }
      if (value && value.duration != null) {
        value.duration /= 1000;
      }
      return value;
    });
  },
});
