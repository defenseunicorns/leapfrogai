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
  <path d="M14,31.36H2	c-0.199,0-0.36-0.161-0.36-0.36V11c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v20	C14.36,31.199,14.199,31.36,14,31.36z M2.36,30.64h11.28V11.36H2.36V30.64z M30,31.36H18c-0.199,0-0.36-0.161-0.36-0.36V1	c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v30C30.36,31.199,30.199,31.36,30,31.36z M18.36,30.64h11.28V1.36	H18.36V30.64z M6.36,14H5.64v2h0.72C6.36,16,6.36,14,6.36,14z M10.36,14H9.64v2h0.72C10.36,16,10.36,14,10.36,14z M6.36,19H5.64v2	h0.72C6.36,21,6.36,19,6.36,19z M10.36,19H9.64v2h0.72C10.36,21,10.36,19,10.36,19z M6.36,24H5.64v2h0.72C6.36,26,6.36,24,6.36,24z M10.36,24H9.64v2h0.72C10.36,26,10.36,24,10.36,24z M22.36,14h-0.72v2h0.721L22.36,14L22.36,14z M22.36,9h-0.72v2h0.721L22.36,9	L22.36,9z M26.36,14h-0.72v2h0.721L26.36,14L26.36,14z M26.36,9h-0.72v2h0.721L26.36,9L26.36,9z M22.36,4h-0.72v2h0.721L22.36,4	L22.36,4z M26.36,4h-0.72v2h0.721L26.36,4L26.36,4z M22.36,19h-0.72v2h0.721L22.36,19L22.36,19z M26.36,19h-0.72v2h0.721L26.36,19	L26.36,19z M22.36,24h-0.72v2h0.721L22.36,24L22.36,24z M26.36,24h-0.72v2h0.721L26.36,24L26.36,24z"></path>
</svg>