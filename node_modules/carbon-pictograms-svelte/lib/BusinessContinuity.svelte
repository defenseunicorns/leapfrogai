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
  <path d="M25,22.36c-3.382,0-6.07-2.901-6.261-3.112l-1.994-1.993l0.509-0.509l2,2l0.013,0.015	c0.026,0.028,2.623,2.88,5.732,2.88c3.11,0,5.64-2.529,5.64-5.64c0-3.11-2.529-5.64-5.64-5.64c-2.114,0-3.897,1.202-4.771,1.918	l-0.457-0.557C20.721,10.944,22.662,9.64,25,9.64c3.507,0,6.36,2.853,6.36,6.36S28.507,22.36,25,22.36z M12.732,13.24	c-0.026-0.029-2.623-2.88-5.732-2.88c-3.11,0-5.64,2.53-5.64,5.64S3.89,21.64,7,21.64c2.115,0,3.897-1.201,4.772-1.918l0.456,0.557	C11.28,21.056,9.339,22.36,7,22.36c-3.507,0-6.36-2.854-6.36-6.36S3.493,9.64,7,9.64c3.382,0,6.071,2.901,6.261,3.112l1.993,1.994	l-0.509,0.509l-2-2L12.732,13.24z M13.254,19.255l-0.509-0.51l5.385-5.385H16v-0.72h3.36V16h-0.72v-2.131L13.254,19.255z"></path>
</svg>