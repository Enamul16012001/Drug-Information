# Drug Search Application

A clean and attractive web application to search the FDA's Drugs@FDA database with universal search capability.

## Features

- **Universal Search** - Search across all fields at once without specifying a category
- Search by Brand Name
- Search by Generic Name
- Search by Application Number (NDA/ANDA/BLA)
- Search by Manufacturer
- Search by Active Ingredient
- Advanced search with custom fields
- Attractive, modern interface with animations
- Real-time results display
- Collapsible advanced options

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

### Universal Search (Recommended)
- Simply type any drug name, manufacturer, or ingredient in the main search box
- Click "Search Everything" to search across all fields automatically
- No need to specify what type of information you're searching for

### Quick Examples
- Click on any example term (Aspirin, Pfizer, etc.) for instant results

### Advanced Search (Optional)
- Click "Show Advanced Search Options" for targeted searches
- Choose specific fields for more precise results
- Use custom field search for specialized queries

## API Endpoints

- `GET /api/search/all?query={term}&limit={num}` - Universal search across all fields
- `GET /api/search?query={term}&field={field}&limit={num}` - Field-specific search
- `GET /api/application/{app_number}` - Search by application number
- `GET /api/manufacturer?name={name}&limit={num}` - Search by manufacturer
- `GET /api/active-ingredient?name={name}&limit={num}` - Search by active ingredient

## Available Search Fields

- openfda.brand_name - Brand or trade name
- openfda.generic_name - Generic name
- openfda.manufacturer_name - Manufacturer name
- openfda.substance_name - Active ingredients
- openfda.route - Route of administration
- products.dosage_form - Dosage form (tablet, injection, etc.)
- products.marketing_status - Marketing status
- openfda.pharm_class_epc - Pharmacologic class

## Design Features

- Modern gradient background
- Smooth animations and transitions
- Hover effects on interactive elements
- Mobile-responsive design
- Collapsible advanced options
- Quick search examples
- Color-coded information cards