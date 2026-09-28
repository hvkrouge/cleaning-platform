# MVP Specification

## Customer
- Service catalogue
- Property profile
- Quote
- Slot selection
- Booking
- Payment
- Booking status
- Review

## Partner
- Profile/KYC placeholder
- Availability
- Job feed
- Accept
- Start
- Checklist/photo upload placeholder
- Complete
- Earnings

## Admin
- Dashboard
- Booking list
- Assign partner
- Services/pricing
- Partner list
- Payout visibility

## First real vertical slice
`POST /pricing/quote` → `POST /bookings` → `POST /admin/bookings/{id}/assign` → `POST /partners/{partner_id}/assignments/{assignment_id}/accept` → `POST /partners/{partner_id}/bookings/{booking_id}/start` → `POST /partners/{partner_id}/bookings/{booking_id}/complete`
