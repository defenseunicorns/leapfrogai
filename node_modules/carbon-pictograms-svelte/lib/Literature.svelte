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
  <path d="M31,27.36H18v-0.72h12.64V7h0.721v20	C31.36,27.199,31.199,27.36,31,27.36z M14,27.36H1c-0.199,0-0.36-0.161-0.36-0.36V7h0.72v19.64H14V27.36z M16.36,27h-0.72	c0-0.904-0.736-1.64-1.64-1.64H3c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h11c0.842,0,1.582,0.443,2,1.108	c0.418-0.666,1.158-1.108,2-1.108h11c0.199,0,0.36,0.161,0.36,0.36v20c0,0.199-0.161,0.36-0.36,0.36H18	C17.096,25.36,16.36,26.096,16.36,27z M15.64,7c0-0.904-0.736-1.64-1.64-1.64H3.36v19.28H14c0.637,0,1.215,0.254,1.64,0.665V7z M16.36,7v18.305c0.425-0.411,1.003-0.665,1.64-0.665h10.64V5.36H18C17.096,5.36,16.36,6.096,16.36,7z M27,20.36h-9v-0.72h9V20.36z M14,20.36H5v-0.72h9V20.36z M27,16.36h-9v-0.72h9V16.36z M14,16.36H5v-0.72h9V16.36z M27,12.36h-9v-0.72h9V12.36z M14,12.36H5	v-0.72h9V12.36z M27,8.36h-9V7.64h9V8.36z M14,8.36H5V7.64h9V8.36z"></path>
</svg>