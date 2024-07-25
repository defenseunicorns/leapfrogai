<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { Button, Input, Label } from 'flowbite-svelte';
  import { superForm } from 'sveltekit-superforms';
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

<div class="flex w-full flex-col items-center gap-10 pt-3">
  <div class="h-[72px] w-[252px]">
    <img alt="LeapfrogAI Logo" src={logo} class="logo" />
  </div>
  {#if env.PUBLIC_DISABLE_KEYCLOAK === 'true'}
    <form method="POST" action={isSignup ? '/auth?/signup' : '/auth?/login'} use:enhance>
      <div class="flex flex-col gap-2">
        <Label for="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          bind:value={$form.email}
          placeholder="Your email address"
        />

        <Label for="password">Password</Label>
        <Input
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
      color="alternative"
      on:click={() => {
        isSignup = !isSignup;
      }}>{isSignup ? 'Already have an account? Sign In' : 'Need an account? Sign Up'}</Button
    >
  {:else}
    <Button on:click={signInWithKeycloak}>Log In with UDS SSO</Button>
  {/if}
</div>
