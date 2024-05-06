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
  <path d="M16 11.64H28V12.360000000000001H16zM16 5.64H28V6.359999999999999H16zM4.359 8.002c0-.904.736-1.64 1.64-1.64h3.146L6.931 8.576 7.44 9.084l2.829-2.828c.068-.067.105-.159.105-.254s-.038-.187-.105-.254L7.44 2.919 6.931 3.428l2.214 2.214H6c-1.301 0-2.36 1.059-2.36 2.36v4.5h.72L4.359 8.002 4.359 8.002zM16 17.64H28V18.361H16z"></path><path d="M31,0.64H13c-0.199,0-0.36,0.161-0.36,0.36v13.64H3c-1.301,0-2.36,1.059-2.36,2.36v8c0,1.302,1.059,2.36,2.36,2.36h3.777 l1.901,3.801l0.644-0.322l-2-4C7.261,26.717,7.136,26.64,7,26.64H3c-0.904,0-1.64-0.735-1.64-1.64v-8c0-0.904,0.736-1.64,1.64-1.64 h9.64v4.713C12.267,20.218,12,20.575,12,21s0.267,0.782,0.64,0.927V23c0,0.199,0.161,0.36,0.36,0.36h3.64V25 c0,0.904-0.736,1.64-1.64,1.64H9v0.721h6c1.301,0,2.36-1.059,2.36-2.36v-1.64H31c0.199,0,0.36-0.161,0.36-0.36V1 C31.36,0.801,31.199,0.64,31,0.64z M30.64,22.64H13.36V1.36h17.28V22.64z"></path><circle cx="5" cy="21" r="1"></circle><circle cx="9" cy="21" r="1"></circle>
</svg>