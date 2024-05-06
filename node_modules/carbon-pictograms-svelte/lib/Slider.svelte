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
  <path d="M16,31.36c-1.731,0-3.161-1.316-3.341-3H1v-0.72h11.659c0.18-1.684,1.61-3,3.341-3s3.161,1.316,3.341,3H31	v0.721H19.341C19.161,30.044,17.731,31.36,16,31.36z M16,25.36c-1.456,0-2.64,1.184-2.64,2.64s1.185,2.64,2.64,2.64	c1.456,0,2.64-1.184,2.64-2.64S17.456,25.36,16,25.36z M25,19.36c-1.731,0-3.161-1.316-3.341-3H1v-0.72h20.659	c0.18-1.684,1.609-3,3.341-3s3.161,1.316,3.341,3H31v0.72h-2.659C28.161,18.044,26.731,19.36,25,19.36z M25,13.36	c-1.456,0-2.64,1.185-2.64,2.64c0,1.456,1.184,2.64,2.64,2.64s2.64-1.184,2.64-2.64S26.456,13.36,25,13.36z M7,7.36	c-1.731,0-3.161-1.316-3.341-3H1V3.64h2.659c0.18-1.684,1.61-3,3.341-3s3.161,1.316,3.341,3H31v0.72H10.341	C10.161,6.044,8.731,7.36,7,7.36z M7,1.36C5.544,1.36,4.36,2.544,4.36,4S5.544,6.64,7,6.64S9.64,5.456,9.64,4S8.456,1.36,7,1.36z"></path>
</svg>