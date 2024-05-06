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
  <path d="M26,1.64v0.72h4.131L3.673,28.818C3.474,28.705,3.245,28.64,3,28.64	c-0.75,0-1.36,0.61-1.36,1.36S2.25,31.36,3,31.36S4.36,30.75,4.36,30c0-0.244-0.065-0.475-0.178-0.673L30.64,2.87V7h0.721V1.64H26z M3,30.64c-0.353,0-0.64-0.287-0.64-0.64S2.647,29.36,3,29.36S3.64,29.647,3.64,30S3.353,30.64,3,30.64z M3.36,26H2.64V4	c0-1.853,1.507-3.36,3.36-3.36S9.36,2.147,9.36,4v17H8.64V4c0-1.456-1.185-2.64-2.64-2.64S3.36,2.544,3.36,4V26z M15.36,15h-0.72V4	c0-1.853,1.507-3.36,3.36-3.36S21.36,2.147,21.36,4v5h-0.72V4c0-1.456-1.184-2.64-2.64-2.64S15.36,2.545,15.36,4V15z M14.64,21h0.72	v7c0,1.853-1.507,3.36-3.36,3.36S8.64,29.853,8.64,28v-1h0.72v1c0,1.456,1.185,2.64,2.64,2.64s2.64-1.184,2.64-2.64	C14.64,28,14.64,21,14.64,21z M26.64,9h0.721v19c0,1.853-1.508,3.36-3.36,3.36s-3.36-1.508-3.36-3.36V15h0.721v13	c0,1.456,1.184,2.64,2.64,2.64s2.64-1.184,2.64-2.64V9H26.64z"></path>
</svg>