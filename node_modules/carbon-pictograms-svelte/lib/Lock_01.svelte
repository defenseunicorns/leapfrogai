<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M17.5,20.5c0,0.704-0.486,1.29-1.14,1.452V24c0,0.199-0.161,0.36-0.36,0.36s-0.36-0.161-0.36-0.36v-2.048	c-0.654-0.162-1.14-0.748-1.14-1.452c0-0.828,0.672-1.5,1.5-1.5C16.828,19,17.5,19.672,17.5,20.5z M26.36,21	c0,5.713-4.647,10.36-10.36,10.36c-5.712,0-10.36-4.647-10.36-10.36c0-3.752,2.005-7.045,5-8.863V6c0-2.956,2.404-5.36,5.36-5.36	c2.955,0,5.36,2.404,5.36,5.36v6.137C24.355,13.955,26.36,17.248,26.36,21z M11.36,11.738c1.396-0.703,2.973-1.098,4.64-1.098	s3.243,0.396,4.64,1.098V6c0-2.559-2.081-4.64-4.64-4.64S11.36,3.441,11.36,6V11.738z M25.64,21c0-5.315-4.324-9.64-9.64-9.64	S6.36,15.685,6.36,21s4.325,9.64,9.64,9.64S25.64,26.315,25.64,21z"></path>
</svg>