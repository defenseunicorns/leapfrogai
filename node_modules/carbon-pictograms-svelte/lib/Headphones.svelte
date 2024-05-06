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
  <path d="M27,31.36c-1.302,0-2.36-1.059-2.36-2.36v-8c0-1.302,1.059-2.36,2.36-2.36s2.36,1.059,2.36,2.36v8	C29.36,30.302,28.302,31.36,27,31.36z M27,19.36c-0.904,0-1.64,0.735-1.64,1.64v8c0,0.904,0.735,1.64,1.64,1.64	s1.64-0.735,1.64-1.64v-8C28.64,20.096,27.904,19.36,27,19.36z M5,31.36c-1.301,0-2.36-1.059-2.36-2.36v-8	c0-1.302,1.059-2.36,2.36-2.36S7.36,19.698,7.36,21v8C7.36,30.302,6.301,31.36,5,31.36z M5,19.36c-0.904,0-1.64,0.735-1.64,1.64v8	c0,0.904,0.736,1.64,1.64,1.64S6.64,29.904,6.64,29v-8C6.64,20.096,5.904,19.36,5,19.36z M31.36,25h-0.72v-9	c0-8.073-6.567-14.64-14.64-14.64C7.927,1.36,1.36,7.927,1.36,16v9H0.64v-9C0.64,7.53,7.53,0.64,16,0.64S31.36,7.53,31.36,16V25z"></path>
</svg>