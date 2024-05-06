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
  <path d="M14,31.36c-0.062,0-0.124-0.017-0.18-0.048l-10-5.75	c-0.111-0.064-0.18-0.184-0.18-0.312v-11.5c0-0.129,0.069-0.248,0.18-0.312l10-5.75c0.111-0.064,0.248-0.064,0.359,0l10,5.75	c0.111,0.064,0.181,0.183,0.181,0.312v11.5c0,0.129-0.069,0.248-0.181,0.312l-10,5.75C14.124,31.344,14.062,31.36,14,31.36z M4.36,25.042L14,30.585l9.64-5.543V13.958L14,8.415l-9.64,5.543C4.36,13.958,4.36,25.042,4.36,25.042z M28.36,18h-0.72V6.958	L18,1.415L8.18,7.062L7.82,6.438l10-5.75c0.111-0.064,0.248-0.064,0.359,0l10,5.75C28.29,6.502,28.36,6.621,28.36,6.75	C28.36,6.75,28.36,18,28.36,18z"></path>
</svg>