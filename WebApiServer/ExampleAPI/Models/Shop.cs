﻿using System;
using System.Collections.Generic;

// Code scaffolded by EF Core assumes nullable reference types (NRTs) are not used or disabled.
// If you have enabled NRTs for your project, then un-comment the following line:
// #nullable disable

namespace ExampleAPI.Models
{
    public partial class Shop
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public float Price { get; set; }
        public string Url { get; set; }
    }
}
