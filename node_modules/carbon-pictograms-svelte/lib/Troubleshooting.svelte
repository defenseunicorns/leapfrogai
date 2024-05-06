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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16	S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16	c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M16,24.36c-3.42,0-6.46-2.051-7.747-5.226	l0.667-0.27c1.176,2.9,3.955,4.774,7.08,4.774c4.213,0,7.64-3.427,7.64-7.64h0.721C24.36,20.609,20.609,24.36,16,24.36z M16.36,22	h-0.72v-4.64H15c-0.199,0-0.36-0.161-0.36-0.36v-0.64H10v-0.72h4.64V15c0-0.199,0.161-0.36,0.36-0.36h0.64V10h0.72v4.64H17	c0.199,0,0.36,0.161,0.36,0.36v0.64H22v0.72h-4.64V17c0,0.199-0.161,0.36-0.36,0.36h-0.64V22z M15.36,16.64h1.28v-1.28h-1.28V16.64z M8.36,16H7.64c0-4.61,3.75-8.36,8.36-8.36c3.42,0,6.461,2.051,7.747,5.225l-0.668,0.271C21.904,10.234,19.125,8.36,16,8.36	C11.787,8.36,8.36,11.787,8.36,16z"></path>
</svg>