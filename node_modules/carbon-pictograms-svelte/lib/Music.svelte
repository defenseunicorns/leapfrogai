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
  <path d="M7,30.36c-2.404,0-4.36-1.956-4.36-4.36	S4.596,21.64,7,21.64c1.519,0,2.859,0.781,3.64,1.963V6.795c0-0.163,0.109-0.306,0.267-0.348l18-4.795	c0.105-0.03,0.224-0.006,0.312,0.062C29.308,1.783,29.36,1.888,29.36,2v19c0,2.404-1.956,4.36-4.36,4.36s-4.36-1.956-4.36-4.36	s1.956-4.36,4.36-4.36c1.519,0,2.859,0.781,3.64,1.962V8.468l-17.28,4.604V26C11.36,28.404,9.404,30.36,7,30.36z M7,22.36	c-2.007,0-3.64,1.633-3.64,3.64S4.993,29.64,7,29.64s3.64-1.633,3.64-3.64S9.007,22.36,7,22.36z M25,17.36	c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S27.007,17.36,25,17.36z M11.36,7.072v5.255l17.28-4.604	V2.468L11.36,7.072z"></path>
</svg>