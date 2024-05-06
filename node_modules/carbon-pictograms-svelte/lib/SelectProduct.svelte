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
  <path d="M23,10.509l-2.255-2.255l0.51-0.509L23,9.491l3.745-3.745l0.51,0.509L23,10.509z M30.36,30V18	c0-0.199-0.161-0.36-0.36-0.36H18c-0.199,0-0.36,0.161-0.36,0.36v12c0,0.199,0.161,0.36,0.36,0.36h12	C30.199,30.36,30.36,30.199,30.36,30z M18.36,18.36h11.28v11.28H18.36V18.36z M14.36,30V18c0-0.199-0.161-0.36-0.36-0.36H2	c-0.199,0-0.36,0.161-0.36,0.36v12c0,0.199,0.161,0.36,0.36,0.36h12C14.199,30.36,14.36,30.199,14.36,30z M2.36,18.36h11.28v11.28	H2.36V18.36z M30.36,14V2c0-0.199-0.161-0.36-0.36-0.36H18c-0.199,0-0.36,0.161-0.36,0.36v12c0,0.199,0.161,0.36,0.36,0.36h12	C30.199,14.36,30.36,14.199,30.36,14z M18.36,2.36h11.28v11.28H18.36V2.36z M14.36,14V2c0-0.199-0.161-0.36-0.36-0.36H2	C1.801,1.64,1.64,1.801,1.64,2v12c0,0.199,0.161,0.36,0.36,0.36h12C14.199,14.36,14.36,14.199,14.36,14z M2.36,2.36h11.28v11.28	H2.36V2.36z"></path>
</svg>