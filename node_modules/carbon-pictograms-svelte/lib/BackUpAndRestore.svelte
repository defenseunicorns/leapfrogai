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
  <path d="M31.36,16c0,8.47-6.891,15.36-15.36,15.36	S0.64,24.47,0.64,16c0-7.276,5.168-13.606,12.288-15.052l0.144,0.706C6.286,3.032,1.36,9.065,1.36,16	c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64c0-6.935-4.925-12.968-11.711-14.346l0.143-0.706	C26.192,2.394,31.36,8.724,31.36,16z M11.254,18.745l-0.509,0.51L16,24.509l5.255-5.254l-0.51-0.51l-4.385,4.386V1h-0.72v22.131	L11.254,18.745z"></path>
</svg>