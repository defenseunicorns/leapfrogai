<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { superForm } from 'sveltekit-superforms';
  import { Button } from 'carbon-components-svelte';
  import { env } from '$env/dynamic/public';

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
  const { form, errors, enhance } = superForm(data.form);
</script>

<div class="login-container">
  <div class="logo">
    <img alt="LeapfrogAI Logo" src={logo} class="logo" />
  </div>
  {#if env.PUBLIC_DISABLE_KEYCLOAK === 'true'}
    <form method="POST" action={isSignup ? '/auth?/signup' : '/auth?/login'} use:enhance>
      <div class="form">
        <label for="email"> Email </label>
        <input
          id="email"
          name="email"
          type="email"
          bind:value={$form.email}
          placeholder="Your email address"
        />

        <label for="password"> Password</label>
        <input
          id="password"
          name="password"
          type="password"
          placeholder="Your password"
          bind:value={$form.password}
        />

        <Button type="submit">{isSignup ? 'Sign Up' : 'Sign In'}</Button>
        {#if $errors.email}
          <span style="color: red">{$errors.email}</span>
        {/if}
      </div>
    </form>

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
    gap: 2.5rem;
    width: 100%;
    padding-top: 0.75rem;
  }
  .form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
</style>
