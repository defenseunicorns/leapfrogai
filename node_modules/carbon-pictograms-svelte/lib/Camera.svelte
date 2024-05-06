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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V5c0-0.199,0.161-0.36,0.36-0.36h2.64V1	c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v3.64H31c0.199,0,0.36,0.161,0.36,0.36v26	C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28V5.36H1.36V30.64z M4.36,4.64h11.28V1.36H4.36V4.64z M16,26.36	c-4.058,0-7.36-3.302-7.36-7.36s3.302-7.36,7.36-7.36c4.059,0,7.36,3.302,7.36,7.36C23.36,23.059,20.059,26.36,16,26.36z M16,12.36	c-3.661,0-6.64,2.979-6.64,6.64s2.979,6.64,6.64,6.64s6.64-2.979,6.64-6.64S19.661,12.36,16,12.36z M28,8.36h-8V7.64h8V8.36z"></path>
</svg>