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
  <path d="M20.591,27.473L18.109,24h1.276l1.777,2.605	h0.041L23.047,24h1.208l-2.469,3.391L24.308,31h-1.275l-1.818-2.74h-0.041L19.208,31H18L20.591,27.473z M25.186,24.618V23.89h1.639	v0.728H25.186z M27.674,26v-0.613h1.1v-2.843h-0.052l-0.871,1.032l-0.47-0.395L28.373,22h1.14v3.387h0.917V26H27.674z M16.36,31	h-0.72V16.36H1v-0.72h14.64V1h0.72v14.64H31v0.72H16.36V31z M14.36,31h-0.72c0-11.813-0.827-12.64-12.64-12.64v-0.72	C13.236,17.64,14.36,18.764,14.36,31z M31,14.36c-12.236,0-13.36-1.124-13.36-13.36h0.721c0,11.813,0.826,12.64,12.64,12.64	L31,14.36L31,14.36z"></path>
</svg>