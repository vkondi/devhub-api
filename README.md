# devhub-api

A comprehensive Python REST API service designed for personal development projects, featuring PostgreSQL integration, RSA encryption services, and Dev.to portfolio management. Deployable on Vercel with modern architecture and security best practices.

## 🌟 Features

### Core Functionality
- **Portfolio Management**: Fetch and display Dev.to blog articles
- **RSA Encryption Service**: Secure encryption/decryption capabilities with industry standards
- **User Authentication**: Project-specific user management with PostgreSQL backend
- **Health Monitoring**: System health check endpoints
- **CORS Support**: Full cross-origin resource sharing configuration

### Security Features
- RSA-OAEP encryption with SHA-256 hashing
- Environment-based configuration management
- Secure API key handling for external services
- Production/development environment detection

## 🛠 Technology Stack

- **Backend**: Flask 2.3.3 with Python
- **Database**: PostgreSQL with psycopg2 driver
- **Security**: Cryptography library for RSA encryption
- **HTTP Client**: Requests library for external API calls
- **Deployment**: Vercel serverless platform
- **Development**: Flask-CORS, python-dotenv

## 📡 API Endpoints

### Health Check
- `GET /api/v1/health` - System health status

### Portfolio Management
- `GET /api/v1/portfolio/blogs` - Fetch Dev.to articles

### Authentication & Encryption
- `GET /api/v1/auth/public_key` - Retrieve RSA public key
- `GET /api/v1/auth/encrypt_test/<plaintext>` - Test encryption (development only)
- `POST /api/v1/auth/decrypt_test` - Test decryption (development only)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Dev.to API key
- RSA key pair (public/private)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vkondi/devhub-api.git
   cd devhub-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/devhub

# Dev.to API Configuration
DEV_TO_API_KEY=your_devto_api_key_here

# RSA Keys (generate these using openssl)
RSA_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----

RSA_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
YOUR_PUBLIC_KEY_HERE
-----END PUBLIC KEY-----

# Environment Configuration
ENV=development  # or 'production'
```

### Generate RSA Keys

```bash
# Generate private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Generate public key
openssl rsa -pubout -in private_key.pem -out public_key.pem

# Copy the contents into your .env file
```

### Running the Application

**Local Development:**
```bash
python api/app.py
```

The server will start on `http://localhost:5328`

**Vercel Deployment:**
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

## 🔧 Development

### Adding New Endpoints

1. Create a new route file in `api/routes/`
2. Define your Blueprint and endpoints
3. Register the Blueprint in `api/app.py`
4. Add corresponding services in `api/services/` if needed

### Database Migrations

Currently, the database is initialized automatically on startup. For production, consider implementing Alembic for proper database migrations.

### Testing

To run tests (when implemented):
```bash
python -m pytest
```

## 🚀 Deployment

### Vercel Configuration

The project is pre-configured for Vercel deployment:

1. **Automatic Deployment**: Connect to GitHub repository
2. **Environment Variables**: Set in Vercel dashboard
3. **Serverless Functions**: Each route becomes a serverless function

### Environment-Specific Behavior

- **Development**: Full debug mode, local database, test endpoints enabled
- **Production**: Optimized for performance, production database, test endpoints disabled

## 🔒 Security Considerations

- RSA encryption uses OAEP padding with SHA-256
- Environment variables are used for sensitive data
- CORS is configured for cross-origin requests
- Database connections use secure connection strings
- Test endpoints should be disabled in production

## 📈 API Usage Examples

### Fetch Dev.to Articles
```bash
curl http://localhost:5328/api/v1/portfolio/blogs
```

### Get RSA Public Key
```bash
curl http://localhost:5328/api/v1/auth/public_key
```

### Test Encryption
```bash
curl http://localhost:5328/api/v1/auth/encrypt_test/hello
```

### Test Decryption
```bash
curl -X POST http://localhost:5328/api/v1/auth/decrypt_test \
  -H "Content-Type: application/json" \
  -d '{"ciphertext": "encrypted_base64_string"}'
```

## 🛣 Roadmap

### Planned Improvements

**High Priority:**
- [ ] JWT authentication implementation
- [ ] Remove test endpoints from production
- [ ] Comprehensive error handling
- [ ] Database connection pooling

**Medium Priority:**
- [ ] API documentation with OpenAPI/Swagger
- [ ] Caching layer implementation
- [ ] Comprehensive test suite
- [ ] Structured logging system

**Low Priority:**
- [ ] FastAPI migration consideration
- [ ] Monitoring and analytics
- [ ] Additional platform integrations (GitHub, Medium)
- [ ] Advanced portfolio features

### Future Features
- Multi-platform content aggregation
- User authentication and profiles
- Advanced caching strategies
- Real-time notifications
- Analytics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the existing documentation
- Review the code comments for additional context

## 📊 Monitoring

### Health Checks
The `/api/v1/health` endpoint provides basic system health information. Future versions will include:
- Database connectivity status
- External API availability
- System metrics and performance indicators

---

Built with ❤️ for personal development projects and portfolio management.
