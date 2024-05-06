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
  <path d="M27.255,30.255l-0.51-0.51	L30.491,26l-3.746-3.745l0.51-0.51L31.509,26L27.255,30.255z M18.745,30.255L14.491,26l4.254-4.255l0.51,0.51L15.509,26l3.746,3.745	L18.745,30.255z M21.334,31.134l-0.668-0.268l4-10l0.668,0.268L21.334,31.134z M13,30.36H1c-0.199,0-0.36-0.161-0.36-0.36V2	c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v28C13.36,30.199,13.199,30.36,13,30.36z M1.36,29.64h10.56	L1.36,21.72V29.64z M1.6,21l11.04,8.28V12.72L1.6,21z M1.36,2.769V20.28l11.06-8.295L1.36,2.769z M1.994,2.36l10.646,8.872V2.36	H1.994z M29.36,19h-0.72V2.36H17.36V19h-0.72V2c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36	C29.36,2,29.36,19,29.36,19z"></path>
</svg>