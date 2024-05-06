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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16	S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M9.36,29.046c1.994,1.019,4.251,1.594,6.64,1.594	s4.646-0.575,6.64-1.594V16.36h-5.328c-0.158,0.576-0.686,1-1.312,1c-0.75,0-1.36-0.61-1.36-1.36s0.61-1.36,1.36-1.36	c0.625,0,1.153,0.424,1.312,1h5.328V7.36H9.36V29.046z M23.36,16.36v12.292c4.253-2.484,7.148-7.052,7.275-12.292H23.36z M16,1.36	C7.927,1.36,1.36,7.927,1.36,16c0,5.392,2.93,10.111,7.28,12.652V7c0-0.199,0.161-0.36,0.36-0.36h14c0.199,0,0.36,0.161,0.36,0.36	v8.64h7.275C30.444,7.733,23.952,1.36,16,1.36z M16,15.36c-0.353,0-0.64,0.287-0.64,0.64s0.287,0.64,0.64,0.64s0.64-0.287,0.64-0.64	S16.353,15.36,16,15.36z"></path>
</svg>