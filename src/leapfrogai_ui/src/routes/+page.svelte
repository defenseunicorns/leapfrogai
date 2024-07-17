<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { Button } from 'carbon-components-svelte';
  import { Auth } from '@supabase/auth-ui-svelte';
  import { env } from '$env/dynamic/public';
  import { ThemeSupa } from '@supabase/auth-ui-shared';

  export let data;
  export let queryParams: { [key: string]: string } | undefined = undefined;

  let isSignup = true;
  let { supabase, url } = data;
  $: ({ supabase, url } = data);

  async function signInWithKeycloak() {
    await supabase.auth.signInWithOAuth({
      provider: 'keycloak',
      options: {
        scopes: 'openid',
        redirectTo: `${url}/auth/callback`,
        queryParams
      }
    });
  }
</script>

<div class="login-container">
  <div class="logo">
    <img alt="LeapfrogAI Logo" src={logo} class="logo" />
  </div>
  {#if env.PUBLIC_DISABLE_KEYCLOAK === 'true'}
    <Auth
      supabaseClient={data.supabase}
      view={isSignup ? 'sign_up' : 'sign_in'}
      redirectTo={`${data.url}/auth/callback`}
      showLinks={false}
      appearance={{ theme: ThemeSupa, style: { input: 'color: #fff' } }}
    />
    <Button
      kind="ghost"
      on:click={() => {
        isSignup = !isSignup;
      }}>{isSignup ? 'Already have an account? Sign In' : 'Need an account? Sign Up'}</Button
    >
  {:else}
    <Button on:click={signInWithKeycloak} kind="secondary">Log In with UDS SSO</Button>
  {/if}
</div>

<style lang="scss">
  .logo {
    width: 252px;
    height: 72px;
  }
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: layout.$spacing-08;
    width: 100%;
    padding-top: layout.$spacing-04;
  }
</style>
