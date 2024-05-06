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
  <path d="M16,30.36c-3.938,0-7.163-3.108-7.351-7H5	c-0.129,0-0.249-0.069-0.312-0.182l-4-7c-0.063-0.111-0.063-0.247,0-0.357l4-7C4.751,8.709,4.871,8.64,5,8.64h3.649	c0.188-3.892,3.414-7,7.351-7s7.163,3.108,7.352,7H27c0.129,0,0.248,0.069,0.312,0.181l4,7c0.063,0.111,0.063,0.247,0,0.357l-4,7	C27.248,23.291,27.129,23.36,27,23.36h-3.648C23.163,27.252,19.938,30.36,16,30.36z M23.352,9.36c-0.188,3.892-3.414,7-7.352,7	c-3.661,0-6.64,2.979-6.64,6.64s2.979,6.64,6.64,6.64s6.64-2.979,6.64-6.64c0-0.199,0.161-0.36,0.36-0.36h3.791L30.585,16	l-3.794-6.64C26.791,9.36,23.352,9.36,23.352,9.36z M5.209,22.64h3.44c0.188-3.892,3.414-7,7.351-7c3.661,0,6.64-2.979,6.64-6.64	S19.661,2.36,16,2.36S9.36,5.339,9.36,9c0,0.199-0.161,0.36-0.36,0.36H5.209L1.415,16L5.209,22.64z"></path>
</svg>