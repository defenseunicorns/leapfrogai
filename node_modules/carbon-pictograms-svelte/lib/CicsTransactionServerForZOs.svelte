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
  <path d="M18,28.36h-8v-0.72h8	c5.315,0,9.64-4.324,9.64-9.64v-4h0.721v4C28.36,23.713,23.713,28.36,18,28.36z M4,24.36c-1.301,0-2.36-1.059-2.36-2.36	S2.699,19.64,4,19.64S6.36,20.698,6.36,22S5.301,24.36,4,24.36z M4,20.36c-0.904,0-1.64,0.735-1.64,1.64S3.096,23.64,4,23.64	S5.64,22.904,5.64,22S4.904,20.36,4,20.36z M16,20.36c-2.404,0-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36s4.36,1.956,4.36,4.36	S18.404,20.36,16,20.36z M16,12.36c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64S18.007,12.36,16,12.36	z M4.36,18H3.64v-4C3.64,8.288,8.288,3.64,14,3.64h8v0.72h-8c-5.315,0-9.64,4.325-9.64,9.64C4.36,14,4.36,18,4.36,18z M28,12.36	c-1.302,0-2.36-1.059-2.36-2.36S26.698,7.64,28,7.64s2.36,1.059,2.36,2.36S29.302,12.36,28,12.36z M28,8.36	c-0.904,0-1.64,0.736-1.64,1.64s0.735,1.64,1.64,1.64s1.64-0.736,1.64-1.64S28.904,8.36,28,8.36z"></path>
</svg>