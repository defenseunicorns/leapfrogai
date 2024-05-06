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
  <path d="M25,8.64c-3.507,0-6.36,2.853-6.36,6.36v10c0,3.11-2.53,5.64-5.64,5.64S7.36,28.11,7.36,25v-5.658	c3.339-0.188,6-2.957,6-6.342V5c0-0.199-0.161-0.36-0.36-0.36h-2.64V1c0-0.199-0.161-0.36-0.36-0.36S9.64,0.801,9.64,1v3.64H4.36V1	c0-0.199-0.161-0.36-0.36-0.36S3.64,0.801,3.64,1v3.64H1C0.801,4.64,0.64,4.801,0.64,5v8c0,3.385,2.661,6.154,6,6.342V25	c0,3.507,2.853,6.36,6.36,6.36s6.36-2.854,6.36-6.36V15c0-3.11,2.529-5.64,5.64-5.64s5.64,2.53,5.64,5.64v10h0.721V15	C31.36,11.493,28.507,8.64,25,8.64z M1.36,5.36h11.28v3.28H1.36V5.36z M1.36,13V9.36h11.28V13c0,3.11-2.53,5.64-5.64,5.64	S1.36,16.11,1.36,13z"></path>
</svg>